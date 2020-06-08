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
    monthlyCostHealth: number;
    monthlyCostHome: number;
    monthlyCostTaxes: number;
    commuteTime: number;
    monthlyCostTotal: number;
    yearlyCostTotal: number;
  }

export default TownInfo;