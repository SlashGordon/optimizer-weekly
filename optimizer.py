import multiprocessing as mp
import os
import math

from pystockfilter.tool.start_chunked_optimizer import StartChunkedOptimizer
from pystockfilter.tool.start_seq_optimizer import StartSequentialOptimizer as sso
from pystockfilter.strategy.rsi_strategy import RSIStrategy as rsi
from pystockfilter.strategy.atr_strategy import ATRStrategy as atr
from pystockfilter.strategy.macd_strategy import MACDStrategy as macd
from pystockfilter.strategy.doji_rsi_strategy import DojiRsiStrategy as doji_rsi
from pystockfilter.strategy.sma_cross_sma_strategy import (
    SmaCrossSmaStrategy as sma_cross_sma,
)
from pystockfilter.strategy.ema_cross_ema_strategy import (
    EmaCrossEmaStrategy as ema_cross_ema,
)
from pystockfilter.strategy.uo_strategy import (
    UltimateStrategy as uo_strategy,
)
from pystockfilter.strategy.moving_average_rsi_strategy import (
    MovingAverageRSIStrategy as ma_rsi,
)
from pystockfilter.data.stock_data_source import DataSourceModule as Data
from pystockfilter.tool.start_chunked_optimizer import StartChunkedOptimizer

CHUNKS = int(os.environ.get("CHUNKS_SIZE", 20))
CHUNKS_IDX = int(os.environ.get("CHUNKS_IDX", 1))
# Set multiprocessing method to "fork" for optimized parallel processing in Unix-based systems.
mp.set_start_method("fork")

dax_symbols = [
    "ADS.F",
    "AIR.F",
    "ALV.F",
    "BAS.F",
    "BAYN.F",
    "BEI.F",
    "BMW.F",
    "BNR.F",
    "CBK.F",
    "CON.F",
    "1COV.F",
    "DTG.F",
    "DBK.F",
    "DB1.F",
    "DHL.F",
    "DTE.F",
    "EOAN.F",
    "FRE.F",
    "HNR1.F",
    "HEI.F",
    "HEN3.F",
    "IFX.F",
    "MBG.F",
    "MRK.F",
    "MTX.F",
    "MUV2.F",
    "P911.F",
    "PAH3.F",
    "QIA.F",
    "RHM.F",
    "RWE.F",
    "SAP.F",
    "SRT3.F",
    "SIE.F",
    "ENR.F",
    "SHL.F",
    "SY1.F",
    "VOW3.F",
    "VNA.F",
    "ZAL.F",
]

mda_symbols = [
    "AIXA.F",
    "AT1.F",
    "NDA.F",
    "BC8.F",
    "BFSA.F",
    "GBF.F",
    "AFX.F",
    "EVD.F",
    "DHER.F",
    "LHA.F",
    "EVK.F",
    "FRA.F",
    "FNTN.F",
    "FME.F",
    "FPE3.F",
    "G1A.F",
    "GXI.F",
    "HLE.F",
    "HFG.F",
    "HAG.F",
    "HOT.F",
    "BOSS.F",
    "HYQ.F",
    "JEN.F",
    "JUN3.F",
    "SDF.F",
    "KGX.F",
    "KBX.F",
    "KRN.F",
    "LXS.F",
    "LEG.F",
    "NEM.F",
    "NDX1.F",
    "PUM.F",
    "RAA.F",
    "RDC.F",
    "RRTL.F",
    "1SXP.F",
    "G24.F",
    "WAF.F",
    "STM.F",
    "SAX.F",
    "TEG.F",
    "TLX.F",
    "TMV.F",
    "TKA.F",
    "8TRA.F",
    "TUI1.F",
    "UTDI.F",
    "WCH.F",
]

sdax_symbols = [
    "1U1.F",
    "ADN1.F",
    "ATN.F",
    "ADV.F",
    "ACT.F",
    "AAD.F",
    "AOF.F",
    "AG1.F",
    "BVB.F",
    "COK.F",
    "CEC.F",
    "CWC.F",
    "COP.F",
    "DMP.F",
    "DBAN.F",
    "DEQ.F",
    "PBB.F",
    "DWNI.F",
    "DEZ.F",
    "DOU.F",
    "DRW3.F",
    "DUE.F",
    "DWS.F",
    "EUZ.F",
    "ELG.F",
    "ECV.F",
    "EKT.F",
    "EVT.F",
    "FIE.F",
    "FTK.F",
    "GFT.F",
    "GYC.F",
    "GLJ.F",
    "HABA.F",
    "HDD.F",
    "HBH.F",
    "INH.F",
    "IOS.F",
    "JST.F",
    "KCO.F",
    "KTN.F",
    "KSB3.F",
    "KWS.F",
    "ILM1.F",
    "B4B.F",
    "MLP.F",
    "MUX.F",
    "NA9.F",
    "NOEJ.F",
    "PAT.F",
]
all_symbols = dax_symbols + mda_symbols + sdax_symbols

# Symbols to optimize for the current chunk
start_idx = len(all_symbols) // CHUNKS * (CHUNKS_IDX - 1)
end_idx = len(all_symbols) // CHUNKS * CHUNKS_IDX
symbols = all_symbols[start_idx:end_idx]


parameters = [
    # Strategy: RSI Strategy
    [
        {
            "para_rsi_window": range(5, 25, 1),
        },
        {
            "para_rsi_enter": range(10, 50, 1),
            "para_rsi_exit": range(50, 90, 1),
            "constraint": lambda p: p.para_rsi_enter < p.para_rsi_exit,
        },
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
        },
    ],
    # Strategy: Ultimate Oscillator (UO) Strategy
    [
        {
            "para_uo_upper": range(20, 100, 1),
            "para_uo_lower": range(-30, 50, 1),
            "constraint": lambda p: (p.para_uo_upper > p.para_uo_lower)
            and (p.para_uo_upper - p.para_uo_lower) > 10,
        },
        {
            "para_uo_short": range(7, 30, 1),
            "para_uo_medium": range(14, 40, 1),
            "para_uo_long": range(28, 80, 1),
            "constraint": lambda p: (
                p.para_uo_long > p.para_uo_medium > p.para_uo_short
            )
            and (p.para_uo_long - p.para_uo_medium) > 5
            and (p.para_uo_medium - p.para_uo_short) > 3,
        },
    ],
    # Strategy: SMA Cross SMA Strategy
    [sma_cross_sma.get_optimizer_parameters()],
    # Strategy: EMA Cross EMA Strategy
    [ema_cross_ema.get_optimizer_parameters()],
    # Strategy: ATR Strategy
    [
        {
            "para_atr_window": range(10, 50, 1),
        },
        {
            "constraint": lambda p: p.para_atr_enter > p.para_atr_exit,
            "para_atr_enter": [x / 10 for x in range(10, 50)],  # e.g., 1.0 to 5.0
            "para_atr_exit": [x / 10 for x in range(5, 25)],  # e.g., 0.5 to 2.5
        },
    ],
    # Strategy: MACD Strategy
    [
        macd.get_optimizer_parameters(),
    ],
    # Strategy: Doji RSI Strategy
    [
        doji_rsi.get_optimizer_parameters(),
    ],
]

my_optimizer = StartChunkedOptimizer(
    ticker_symbols=symbols,
    strategies=[
        rsi,
        ma_rsi,
        uo_strategy,
        sma_cross_sma,
        ema_cross_ema,
        atr,
        macd,
        doji_rsi,
    ],
    optimizer_class=sso,
    optimizer_parameters=parameters,
    data_source=Data(Data.Y_FINANCE_CACHE),
    data_chunk_size=300,
)

results = my_optimizer.run(history_months=30)

results.dump_optimization_results(f"result_{CHUNKS_IDX}.json", True, True)
