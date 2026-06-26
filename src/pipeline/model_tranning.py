from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import dataTransformation
from src.components.model_evoulation import modelEvoulation
from src.components.model_training import modelTranning
from src.logger import logging

symbols=['ADBL', 'AHL', 'AHPC', 'AKJCL', 'AKPL', 'ALBSL', 'ALICL', 'ANLB', 'API', 'AVYAN', 'BARUN', 'BBC', 'BEDC', 'BFC', 'BGWT', 'BHDC', 'BHL', 'BHPL', 'BNHC', 'BNL', 'BNT', 'BPCL', 'BPW', 'CBBL', 'CFCL', 'CGH', 'CHCL', 'CHDC', 'CHL', 'CIT', 'CITY', 'CKHL', 'CLI', 'CORBL', 'CYCL', 'CZBIL', 'DDBL', 'DHPL', 'DLBS', 'DOLTI', 'DORDI', 'EBL', 'EDBL', 'EHPL', 'ENL', 'FMDBL', 'FOWAD', 'GBBL', 'GBIME', 'GBLBS', 'GCIL', 'GFCL', 'GHL', 'GILB', 'GLBSL', 'GLH', 'GMFBS', 'GMFIL', 'GRDBL', 'GUFL', 'GVL', 'HATHY', 'HBL', 'HDHPC', 'HDL', 'HEI', 'HHL', 'HIDCL', 'HIDCLP', 'HLBSL', 'HLI', 'HPPL', 'HRL', 'HURJA', 'ICFC', 'IGI', 'IHL', 'ILBS', 'ILI', 'JALPA', 'JBBL', 'JBLB', 'JFL', 'JOSHI', 'JSLBB', 'KBL', 'KBSH', 'KDL', 'KKHC', 'KMCDB', 'KPCL', 'KRBL', 'KSBBL', 'LBBL', 'LEC', 'LICN', 'LSL', 'MAKAR', 'MANDU', 'MBJC', 'MBL', 'MCHL', 'MDB', 'MEHL', 'MEL', 'MEN', 'MERO', 'MFIL', 'MHCL', 'MHL', 'MHNL', 'MKCL', 'MKHC', 'MKHL', 'MKJC', 'MKLB', 'MLBBL', 'MLBL', 'MLBS', 'MMFDB', 'MMKJL', 'MNBBL', 'MPFL', 'MSHL', 'NABBC', 'NABIL', 'NADEP', 'NBL', 'NESDO', 'NFS', 'NGPL', 'NHDL', 'NHPC', 'NIBSF2', 'NICA', 'NICFC', 'NICL', 'NICLBSL', 'NIFRA', 'NIMB', 'NIMBPO', 'NLBBL', 'NLG', 'NLIC', 'NLICL', 'NMB', 'NRIC', 'NRM', 'NRN', 'NSIF2', 'NTC', 'NUBL', 'NWCL', 'NYADI', 'OHL', 'PCBL', 'PFL', 'PHCL', 'PMHPL', 'PMLI', 'PPCL', 'PPL', 'PRIN', 'PROFL', 'PRVU', 'RADHI', 'RAWA', 'RBCL', 'RFPL', 'RHGCL', 'RHPL', 'RIDI', 'RLFL', 'RNLI', 'RSDC', 'RURU', 'SADBL', 'SAHAS', 'SALICO', 'SAMAJ', 'SANIMA', 'SAPDBL', 'SBI', 'SBL', 'SCB', 'SFCL', 'SGHC', 'SGIC', 'SHEL', 'SHINE', 'SHIVM', 'SHL', 'SHLB', 'SHPC', 'SICL', 'SIFC', 'SIKLES', 'SINDU', 'SJCL', 'SJLIC', 'SKBBL', 'SMATA', 'SMB', 'SMH', 'SMHL', 'SMJC', 'SNLI', 'SONA', 'SPC', 'SPDL', 'SPHL', 'SPIL', 'SPL', 'SRLI', 'SSHL', 'STC', 'SWBBL', 'SWMF', 'TAMOR', 'TPC', 'TRH', 'TSHL', 'TVCL', 'UAIL', 'UHEWA', 'ULBSL', 'ULHC', 'UMHL', 'UMRH', 'UNHPL', 'UPCL', 'UPPER', 'USHEC', 'USHL', 'USLB', 'VLBS', 'VLUCL', 'ACLBSL', 'ADBLD83', 'ALICLP', 'BOKD86', 'C30MF', 'CBLD88', 'CCBD88', 'CIZBD86', 'CMF1', 'CMF2', 'EBLD85', 'GBBD85', 'GIBF1', 'H8020', 'HEIP', 'JBBD87', 'KDBY', 'KEF', 'KLBSL', 'KSBBLD87', 'LBLD88', 'LEMF', 'LLBS', 'LUK', 'LVF2', 'MBLD87', 'MLBSL', 'MMF1', 'MSLB', 'NBF2', 'NBF3', 'NBLD85', 'NBLD87', 'NCCD86', 'NIBD2082', 'NIBD84', 'NIBLGF', 'NICAD8283', 'NICBF', 'NICD83/84', 'NICGF', 'NICGF2', 'NICSF', 'NIL', 'NMB50', 'NMBD87/88', 'NMBMF', 'NMFBS', 'PBD85', 'PBD88', 'PBLD87', 'PRSF', 'PSF', 'RBCLPO', 'RMF1', 'RMF2', 'SABSL', 'SAEF', 'SAGF', 'SALICOPO', 'SBCF', 'SBD87', 'SBID83', 'SBID89', 'SDBD87', 'SDLBSL', 'SEF', 'SFEF', 'SFMF', 'SIGS2', 'SIGS3', 'SLBBL', 'SLBSL', 'SLCF', 'SMFBS', 'SWMFPO', 'UNL', 'UNLB', 'WNLB', 'GWFD83', 'ICFCD83', 'KBLD86', 'LBLD86', 'MBLD2085', 'PBLD86', 'EBLD86', 'GBILD86/87', 'HBLD86', 'NRICP', 'PBLD84', 'PCBLP', 'GBD80/81', 'HBLD83', 'JFLPO', 'SRBLD83', 'KBLD89', 'MFLD85', 'MMFDBP', 'SBLD2082', 'KBLPO', 'SINDUP', 'LBBLPO', 'MPFLPO', 'SBLD83', 'SAND2085', 'JBBLPO', 'RLFLPO', 'MNBBLP', 'NICAD8182', 'SARBTM', 'SBLD84', 'KSBBLP', 'FOWADP', 'MBLPO', 'PRVUPO', 'SRD80', 'ILBSP', 'NLO', 'CZBILP', 'GUFLPO', 'NBLD82', 'NMBPO', 'NABILD87', 'NIMBD90', 'SBIBD86', 'JSLBBP', 'LBBLD89', 'RBBD83', 'GBBLPO', 'NMBD2085', 'SBLD89', 'GBIMEP', 'MFILPO', 'NBBD2085', 'PMLIP', 'SADBLP', 'NIFRAUR85/86', 'MSLBP', 'LSLPO', 'SBLPO', 'VLBSPO', 'MLBLD89', 'SPILPO', 'CIZBD90', 'FMDBLP', 'KSY', 'SCBD', 'NICAD 85/86', 'NICAD85/86', 'SIFCPO', 'SJLICP', 'HBLPO', 'NMLBBL', 'MND84/85', 'NICD88', 'SNMAPO', 'NIFRAP', 'PROFLP', 'NIBLSTF', 'MLBLPO', 'NICAP', 'KLBSLP', 'NILPO', 'SAPDBLP', 'BOKD86KA', 'HLIPO', 'SHINEP', 'GBILD84/85', 'PBD84', 'SBD89', 'UAILPO', 'ALBSLP', 'IGIPO', 'SKBBLP', 'GRDBLP', 'MDBPO', 'NMFBSP', 'NMBD89/90', 'NABBCP', 'SWBBLP', 'KBLD90', 'MATRI', 'SMPDA', 'NFSPO', 'SMATAP', 'UNLBP', 'MATRIP', 'NLICP', 'ACLBSLP', 'NABILP', 'NLICLP', 'SMBPO', 'CBBLPO', 'JBLBP', 'NMLBBLP', 'ICFCPO', 'MNMF1', 'KMCDBP', 'CYCLP', 'SLBBLP', 'SGICP', 'SICLPO', 'GMLI', 'NICLPO', 'EDBLPO', 'SMPDAP', 'GSY', 'BFCPO', 'ICFCD88', 'MLBSLP', 'EBLEB89', 'MLBBLP', 'NMIC', 'CREST', 'GILBPO', 'NMBHF2', 'OMPL', 'WNLBP', 'EBLD91', 'GMFILP', 'MBLEF', 'PURE', 'SRLIP', 'PFLPO', 'RSY', 'NIFRAGED', 'TTL', 'SANVI', 'RBBD2088', 'BHCL', 'GBIMESY2', 'HIMSTAR', 'SBLD2091', 'NICAD2091', 'MABEL', 'HLICF', 'DHEL', 'SAGAR', 'BUNGAL', 'SBID2090', 'BANDIPUR', 'SHINED', 'SWASTIK', 'JHAPA', 'NABILD2089', 'SAIL', 'SYPNL', 'RBBF40', 'SFCLP', 'RSML', 'SABBL', 'CSY', 'HFIN', 'SOHL', 'NSY', 'BJHL', 'SKHL', 'RLEL', 'SKHEL', 'ICFCD89', 'PCIL', 'SIPD', 'MLBSP', 'KHPL', 'RSDCP']

# for symbol in symbols:
ingestion= DataIngestion(symbol="NABIL")
data_path,train_path,test_path=ingestion.initiate_data_ingestion()   


logging.info("ajhjkahjhadjhdsjhjkhjhsajhash")     


transformation= dataTransformation(symbol="NABIL")    
preprocessor_path,Train,Test= transformation.data_transforamtion(train_path,test_path)       


tranning = modelEvoulation(symbol='NABIL')   
tranning.model_evoulation(preprocessor_path,Train,Test)  


model_trann=modelTranning(symbol='NABIL')
model_trann.model_tranning(data_path,preprocessor_path)





