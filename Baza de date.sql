CREATE TABLE `Utilizatori` (
  `codUtilizator` int(8) PRIMARY KEY AUTO_INCREMENT,
  `email` varchar(60) NOT NULL,
  `parola` varchar(256) NOT NULL,
  `rol` int(1) NOT NULL,
  `nume` varchar(50) NOT NULL,
  `prenume` varchar(50) NOT NULL,
  `serieActIdentitate` varchar(2),
  `numarActIdentate` varchar(10) NOT NULL,
  `reseteazaParola` bool NOT NULL
);




CREATE TABLE `Autototurisme` (
  `codAutoturism` int(8) PRIMARY KEY AUTO_INCREMENT,
  `marca` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `valoareOdometru` int(10) NOT NULL,
  `tipAutoturism` int(3) NOT NULL,
  `AnulFabricatiei` int(4) NOT NULL,
  `serieCaroserie` varchar(17) NOT NULL,
  `numarInmatriculare` varchar(10) NOT NULL,
  `culoare` varchar(50) NOT NULL,
  `dataPrimeiImatirculari` date NOT NULL,
  `capacitateCilindrica` int(5) NOT NULL,
  `combustibil` int(1) NOT NULL,
  `numarPropietariAnteriori` int(2) NOT NULL,
  `capacitateRezervorTermic` int(4),
  `capacitateAutonomieBaterie` int(4),
  `putereMotor` int(6) NOT NULL,
  `tipTransmisie` int(1) NOT NULL,
  `status` int(1) NOT NULL
);

CREATE TABLE `tipAutoturisme` (
  `codTipAutoturisme` int(3) PRIMARY KEY AUTO_INCREMENT,
  `denumireTipAutoturisme` varchar(50) NOT NULL
);

CREATE TABLE `AutoturismeDotari` (
  `codAutoturismDotari` int(8) PRIMARY KEY AUTO_INCREMENT,
  `codAutoturism` int(8) NOT NULL,
  `codDotare` int(8) NOT NULL
);

CREATE TABLE `AutoturismeFotografii` (
  `codAutoturismFotografii` int(10) PRIMARY KEY AUTO_INCREMENT,
  `codAutoturism` int(8) NOT NULL,
  `caleDiscFotografie` varchar(256) NOT NULL,
  `fotografiePrincipala` bool NOT NULL
);

CREATE TABLE `Dotari` (
  `codDotare` int(8) PRIMARY KEY AUTO_INCREMENT,
  `denumireDotare` varchar(300) NOT NULL
);

CREATE TABLE `ClientiPersoaneFizice` (
  `codClientPF` int(8) PRIMARY KEY AUTO_INCREMENT,
  `nume` varchar(50) NOT NULL,
  `prenume` varchar(50) NOT NULL,
  `telefon` varchar(10) NOT NULL,
  `CNP` varchar(13),
  `judet` varchar(50),
  `oras` varchar(50),
  `strada` varchar(50),
  `numar` varchar(5),
  `bloc` varchar(5),
  `scara` varchar(5),
  `etaj` varchar(3),
  `appartament` varchar(4)
);

CREATE TABLE `ClientiPersoaneJuridice` (
  `codClientPJ` int(8) PRIMARY KEY AUTO_INCREMENT,
  `Nume` varchar(255) NOT NULL,
  `NumarRegistrulComertului` varchar(255),
  `CUI` varchar(255) NOT NULL,
  `SucursalaBancii` varchar(255) NOT NULL,
  `IBAN` varchar(255) NOT NULL,
  `Tara` varchar(255) NOT NULL,
  `Judet` varchar(255),
  `Oras` varchar(255) NOT NULL,
  `Strada` varchar(255) NOT NULL,
  `Numar` varchar(255) NOT NULL,
  `Scara` varchar(255),
  `Bloc` varchar(255),
  `Etaj` varchar(255),
  `Apartament` varchar(255),
  `numeReprezentant` varchar(50) NOT NULL,
  `prenumeReprezentant` varchar(50) NOT NULL,
  `telefonReprezentant` varchar(10) NOT NULL,
  `CNPReprezentant` varchar(13) NOT NULL,
  `judetReprezentant` varchar(50),
  `orasReprezentant` varchar(50),
  `stradaReprezentant` varchar(50),
  `numarReprezentant` varchar(5),
  `blocReprezentant` varchar(5),
  `scaraReprezentant` varchar(5),
  `etajReprezentant` varchar(3),
  `appartamentReprezentant` varchar(4)
);

CREATE TABLE `Programari` (
  `codProgramare` int(8) PRIMARY KEY AUTO_INCREMENT,
  `tipProgramre` int(1) NOT NULL,
  `dataProgramare` datetime NOT NULL,
  `codAutoturism` int(8),
  `statusProgramre` int(1),
  `codClientPersoanaFizica` int(8),
  `codClientPersoanaJuridica` int(8),
  `codResponsabilIntocmire` int(8) NOT NULL
);

CREATE TABLE `Inspectii` (
  `codInspectie` int(8) PRIMARY KEY AUTO_INCREMENT,
  `codProgramre` int(8) NOT NULL,
  `NumarInmatriculare` varchar(255) NOT NULL,
  `DataInspectiei` datetime NOT NULL,
  `ValoareOdometru` int(10) NOT NULL,
  `codResponsabilIntocmire` int(8) NOT NULL
);

CREATE TABLE `InspectiiTeste` (
  `codInspectieTest` int(8) PRIMARY KEY AUTO_INCREMENT,
  `codInspectie` int(8) NOT NULL,
  `codTest` int(8) NOT NULL,
  `rezultatTest` int(1) NOT NULL,
  `DetaliiTest` varchar(255)
);

CREATE TABLE `CategorieTeste` (
  `codCategorieTeste` int(8) PRIMARY KEY AUTO_INCREMENT,
  `DenumireCategorieTeste` varchar(255)
);

CREATE TABLE `Teste` (
  `codTest` int(8) PRIMARY KEY AUTO_INCREMENT,
  `DenumireTest` varchar(255) NOT NULL
);

CREATE TABLE `TotalTeste` (
  `codTotalTest` int(8) PRIMARY KEY AUTO_INCREMENT,
  `codCategorieTest` int(8) NOT NULL,
  `codTest` int(8) NOT NULL
);

CREATE TABLE `OferteVanzare` (
  `codOferta` int(8) PRIMARY KEY AUTO_INCREMENT,
  `tipOferta` int(1) NOT NULL,
  `codAutorism` int(8) NOT NULL,
  `valoareOdometru` int(10) NOT NULL,
  `pret` float NOT NULL,
  `codInspectieTehnica` int(8) NOT NULL
);

CREATE TABLE `FacturaFiscala` (
  `NumarFactura` int(8) AUTO_INCREMENT,
  `SerieFactura` int(8),
  `ResponsabilIntocmire` int(8),
  PRIMARY KEY (`NumarFactura`, `SerieFactura`)
);

CREATE TABLE `ComponenteFactura` (
  `codComponenteFactura` int(10) AUTO_INCREMENT,
  `NumarFactura` int(8) NOT NULL,
  `SerieFactura` int(8) NOT NULL,
  `codInternContract` int(8),
  `DenumireArticol` varchar(255) NOT NULL,
  `Cantiate` int(4) NOT NULL,
  `PretUnitar` float(5) NOT NULL,
  PRIMARY KEY (`codComponenteFactura`, `NumarFactura`, `SerieFactura`)
);

CREATE TABLE `CertificateGarantie` (
  `numarCertificatGarantie` int(8) PRIMARY KEY AUTO_INCREMENT,
  `codInternContract` int(8),
  `PerioadaGarantie` int(4)
);

CREATE TABLE `ContracteVanzareCumparare` (
  `codInternContract` int(8) PRIMARY KEY AUTO_INCREMENT,
  `vandutDeRadacini` bool,
  `vanzatorPersoanaJuridica` bool,
  `cumparatorPersoanaJuridica` bool,
  `codAutoturism` int(8) NOT NULL,
  `codInternVanzatorPersoanaFizica` int(8),
  `codInternVanzatorPersoanaJuridica` int(8),
  `codInternCumparatorPersaonaFizica` int(8),
  `codInternCumparatorPersaonaJuridica` int(8),
  `codResoinsabilIntocmire` int(8) NOT NULL,
  `valoareaContractului` float(10) NOT NULL,
  `codOferta` int(8)
);

ALTER TABLE `ComponenteFactura` ADD FOREIGN KEY (`NumarFactura`, `SerieFactura`) REFERENCES `FacturaFiscala` (`NumarFactura`, `SerieFactura`);

ALTER TABLE `FacturaFiscala` ADD FOREIGN KEY (`ResponsabilIntocmire`) REFERENCES `Utilizatori` (`codUtilizator`);

ALTER TABLE `AutoturismeDotari` ADD FOREIGN KEY (`codAutoturism`) REFERENCES `Autototurisme` (`codAutoturism`)   ON DELETE CASCADE ON UPDATE CASCADE; 

ALTER TABLE `AutoturismeDotari` ADD FOREIGN KEY (`codDotare`) REFERENCES `Dotari` (`codDotare`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `AutoturismeFotografii` ADD FOREIGN KEY (`codAutoturism`) REFERENCES `Autototurisme` (`codAutoturism`);

ALTER TABLE `Autototurisme` ADD FOREIGN KEY (`tipAutoturism`) REFERENCES `tipAutoturisme` (`codTipAutoturisme`);

ALTER TABLE `Programari` ADD FOREIGN KEY (`codAutoturism`) REFERENCES `Autototurisme` (`codAutoturism`);

ALTER TABLE `Programari` ADD FOREIGN KEY (`codClientPersoanaJuridica`) REFERENCES `ClientiPersoaneJuridice` (`codClientPJ`);

ALTER TABLE `Programari` ADD FOREIGN KEY (`codClientPersoanaFizica`) REFERENCES `ClientiPersoaneFizice` (`codClientPF`);

ALTER TABLE `Inspectii` ADD FOREIGN KEY (`codProgramre`) REFERENCES `Programari` (`codProgramare`);


ALTER TABLE `InspectiiTeste` ADD FOREIGN KEY (`codInspectie`) REFERENCES `Inspectii` (`codInspectie`);

ALTER TABLE `InspectiiTeste` ADD FOREIGN KEY (`codTest`) REFERENCES `Teste` (`codTest`);

ALTER TABLE `OferteVanzare` ADD FOREIGN KEY (`codAutorism`) REFERENCES `Autototurisme` (`codAutoturism`);

ALTER TABLE `OferteVanzare` ADD FOREIGN KEY (`codInspectieTehnica`) REFERENCES `Inspectii` (`codInspectie`);

ALTER TABLE `ComponenteFactura` ADD FOREIGN KEY (`codInternContract`) REFERENCES `ContracteVanzareCumparare` (`codInternContract`);

ALTER TABLE `CertificateGarantie` ADD FOREIGN KEY (`codInternContract`) REFERENCES `ContracteVanzareCumparare` (`codInternContract`);

ALTER TABLE `Programari` ADD FOREIGN KEY (`codResponsabilIntocmire`) REFERENCES `Utilizatori` (`codUtilizator`);

ALTER TABLE `Inspectii` ADD FOREIGN KEY (`codResponsabilIntocmire`) REFERENCES `Utilizatori` (`codUtilizator`);

ALTER TABLE `ContracteVanzareCumparare` ADD FOREIGN KEY (`codResoinsabilIntocmire`) REFERENCES `Utilizatori` (`codUtilizator`);

ALTER TABLE `ContracteVanzareCumparare` ADD FOREIGN KEY (`codOferta`) REFERENCES `OferteVanzare` (`codOferta`);

ALTER TABLE `ContracteVanzareCumparare` ADD FOREIGN KEY (`codInternVanzatorPersoanaJuridica`) REFERENCES `ClientiPersoaneJuridice` (`codClientPJ`);

ALTER TABLE `ContracteVanzareCumparare` ADD FOREIGN KEY (`codInternCumparatorPersaonaJuridica`) REFERENCES `ClientiPersoaneJuridice` (`codClientPJ`);

ALTER TABLE `ContracteVanzareCumparare` ADD FOREIGN KEY (`codInternCumparatorPersaonaFizica`) REFERENCES `ClientiPersoaneFizice` (`codClientPF`);

ALTER TABLE `ContracteVanzareCumparare` ADD FOREIGN KEY (`codInternVanzatorPersoanaFizica`) REFERENCES `ClientiPersoaneFizice` (`codClientPF`);


ALTER TABLE `TotalTeste` ADD FOREIGN KEY (`codCategorieTest`) REFERENCES `CategorieTeste` (`codCategorieTeste`);

ALTER TABLE `TotalTeste` ADD FOREIGN KEY (`codTest`) REFERENCES `Teste` (`codTest`);


ALTER TABLE `radacini_db`.`autoturismedotari` 
DROP FOREIGN KEY `autoturismedotari_ibfk_1`;
ALTER TABLE `radacini_db`.`autoturismedotari` 
ADD CONSTRAINT `autoturismedotari_ibfk_1`
  FOREIGN KEY (`codAutoturism`)
  REFERENCES `radacini_db`.`autototurisme` (`codAutoturism`);


INSERT INTO `Utilizatori` VALUES (
  1,
  'mihai.madalin@gmail.com',
  /*Parola_01 Criptata folosind BCrypt*/
  'scrypt:32768:8:1$n9OVZW1gNXfiDCYO$9025194d58ea3b65e26b69007617fdacff0596a6880ddcb0cc82ceb4b55942af7115232c1ef90d2b75cf513af0f40840eb73541560c351126eb3a5054f435121',
  '4',
  'Neculai',
  'Mihaita Madalin',
  'XR',
  '111111',
  0
  );

  INSERT INTO tipAutoturisme VALUES(1, 'SUV');
  INSERT INTO tipAutoturisme VALUES(2, 'Compact');
  INSERT INTO tipAutoturisme VALUES(3, 'Berlina');
  INSERT INTO tipAutoturisme VALUES(4, 'Break');
  INSERT INTO tipAutoturisme VALUES(5, 'Coupe');
  INSERT INTO tipAutoturisme VALUES(6, 'Decapotabila');

