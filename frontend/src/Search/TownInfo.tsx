interface TownInfo {
    aldi: boolean;
    lidl: boolean;
    coop: boolean;
    migros: boolean;
    sourceTownBFSNr: number;
    sourceTownName: string;
    sourceTownId: number;
    sourceTownZip: number;
    yearlyCostHealth: number;
    yearlyCostHome: number;
    yearlyCostTaxes: number;
    commuteTime: number;
    yearlyCostHealthFormatted: string;
    yearlyCostHomeFormatted: string;
    yearlyCostTaxesFormatted: string;
    commuteTimeFormatted: number;
  }

export default TownInfo;