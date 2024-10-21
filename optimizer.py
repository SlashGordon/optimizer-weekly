import multiprocessing as mp
import os

from pystockfilter.tool.start_chunked_optimizer import StartChunkedOptimizer
from pystockfilter.tool.start_seq_optimizer import StartSequentialOptimizer as sso
from pystockfilter.strategy.rsi_strategy import RSIStrategy as rsi
from pystockfilter.strategy.sma_cross_sma_strategy import SmaCrossSmaStrategy as sma_cross_sma
from pystockfilter.strategy.ema_cross_ema_strategy import EmaCrossEmaStrategy as ema_cross_ema
from pystockfilter.strategy.uo_ema_cross_close_strategy import UltimateEmaCrossCloseStrategy as uo_ema_cross_close
from pystockfilter.strategy.moving_average_rsi_strategy import MovingAverageRSIStrategy as ma_rsi
from pystockfilter.data.stock_data_source import DataSourceModule as Data
from pystockfilter.tool.start_chunked_optimizer import StartChunkedOptimizer

CHUNKS = os.environ.get("CHUNKS_SIZE", 20)
CHUNKS_IDX = os.environ.get("CHUNKS_IDX", 1)
# Set multiprocessing method to "fork" for optimized parallel processing in Unix-based systems.
mp.set_start_method("fork")
dax_symbols = [
    "ADS.F", "AIR.F", "ALV.F", "BAS.F", "BAYN.F", "BMW.F", "BEI.F", "BNR.F", "CON.F", "1COV.F",
    "DBK.F", "DB1.F", "DHL.F", "DTE.F", "DWNI.F", "EOAN.F", "FME.F", "FRE.F", "HEI.F", "HFG.F",
    "HEN.F", "IFX.F", "MBG.F", "MRK.F", "MTX.F", "MUV2.F", "PAH3.F", "PUM.F", "QGEN.F", "RWE.F"
]

mda_symbols = [
  "LHA.F", "ECV.F", "EVK.F", "EVT.F", "FRA.F", "FNTN.F", "FRE.F", 
  "FPE3.F", "G1A.F", "GXI.F", "HLE.F", "HFG.F", "HAG.F", "HOT.F", 
  "BOSS.F", "JEN.F", "JUN3.F", "SDF.F", "KGX.F", "KBX.F", "KRN.F", 
  "LXS.F", "LEG.F", "NEM.F", "NDX1.F", "PUM.F", "RAA.F", "RRTL.F", 
  "S24.F", "SIL.F", "SAX.F", "TGN.F"
]

sdax_symbols = [
  "BFSA.F", "GBF.F", "CEV.F", "DHER.F", "FIE.F", "FRA.F", "HLAG.F", 
  "TKG.F", "HYQ.F", "SKYD.F", "WSU.F", "VZO.F", "VO2.F", "OSR.F", 
  "BOSS.F", "DUE.F", "A1A.F", "LEG.F", "AIXA.F", "NDA.F", "AT1.F"
]

all_symbols = dax_symbols + mda_symbols + sdax_symbols

# Symbols to optimize for the current chunk
symbols = dax_symbols[len(dax_symbols) // CHUNKS * (CHUNKS_IDX - 1):len(dax_symbols) // CHUNKS * CHUNKS_IDX]


parameters = [
    # Strategy: RSI Strategy
    [   
        {
            "para_rsi_window": range(5, 25, 1),
        },
        {
            "para_rsi_enter": range(10, 50, 1),
            "para_rsi_exit": range(50, 90, 1),
            "constraint": lambda p: p.para_rsi_enter < p.para_rsi_exit
        }
    ],
    # Strategy: Moving average + RSI Strategy
    [   
        {
            "para_ma_short": range(2, 20, 1),
            "para_ma_long": range(10, 50, 1),
            "para_rsi_window": 0,
        },
        {
            "para_rsi_window": range(5, 30, 1),
            "para_rsi_threshold": range(20, 100, 1),
        }
    ],
    # Strategy: Ultimate Oscillator (UO) Strategy with EMA Cross Close
    [
        {
            "para_uo_upper": range(20, 100, 1),
            "para_uo_lower": range(-30, 50, 1),
            "para_ema_short": 0,
            "constraint": lambda p: (
                p.para_uo_upper > p.para_uo_lower
            ) and (p.para_uo_upper - p.para_uo_lower) > 10,
            
        },
        {
            "para_uo_short": range(7, 30, 1),
            "para_uo_medium": range(14, 40, 1),
            "para_uo_long": range(28, 80, 1),
            "para_ema_short": 0,
            "constraint": lambda p: (
                p.para_uo_long > p.para_uo_medium > p.para_uo_short
            ) and (p.para_uo_long - p.para_uo_medium) > 5
              and (p.para_uo_medium - p.para_uo_short) > 3,
            
        }, 
        {
            "para_ema_short": range(3, 19, 1),            
        }
    ],
    # Strategy: SMA Cross SMA Strategy
    [
        sma_cross_sma.get_optimizer_parameters()
    ],
    # Strategy: EMA Cross EMA Strategy
    [
        ema_cross_ema.get_optimizer_parameters()
    ],
]

my_optimizer = StartChunkedOptimizer(
    ticker_symbols=dax_symbols[:1],
    strategies=[
        rsi,
        ma_rsi,
        uo_ema_cross_close,
        sma_cross_sma,
        ema_cross_ema,
    ],
    optimizer_class=sso,
    optimizer_parameters=parameters,
    data_source=Data(Data.Y_FINANCE),
    data_chunk_size=300, 
)

results = my_optimizer.run(history_months=30)

results.dump_optimization_results(f"result_{CHUNKS_IDX}.json", True,  True)