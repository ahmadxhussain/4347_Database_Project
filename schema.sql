DROP DATABASE IF EXISTS CorrectionalFacility;
CREATE DATABASE CorrectionalFacility;
USE CorrectionalFacility;

-- 1) Guards
CREATE TABLE Guard (
  GuardID       INT AUTO_INCREMENT PRIMARY KEY,
  Name          VARCHAR(255),
  `Rank`        VARCHAR(50),
  ShiftSchedule VARCHAR(255)
) ENGINE=InnoDB;

-- 2) Cells
CREATE TABLE Cell (
  CellID         INT AUTO_INCREMENT PRIMARY KEY,
  BlockNumber    VARCHAR(50),
  MaxOccupancy   INT,
  SecurityLevel  VARCHAR(50),
  GuardInCharge  INT,
  FOREIGN KEY (GuardInCharge) REFERENCES Guard(GuardID)
) ENGINE=InnoDB;

-- 3) Rehab programs
CREATE TABLE Rehab (
  RehabID     INT AUTO_INCREMENT PRIMARY KEY,
  Name        VARCHAR(255),
  Type        VARCHAR(100),
  Therapy     VARCHAR(100),
  JobTraining VARCHAR(100),
  SuccessRate FLOAT
) ENGINE=InnoDB;

-- 4) Staff
CREATE TABLE Staff (
  StaffID     INT AUTO_INCREMENT PRIMARY KEY,
  Name        VARCHAR(255),
  Role        VARCHAR(100),
  Department  VARCHAR(100),
  StaffType   ENUM('Guard','Doctor','EducationProfessional'),
  RoommateID  INT,
  FOREIGN KEY (RoommateID) REFERENCES Staff(StaffID)
) ENGINE=InnoDB;

-- 5) Lawyers
CREATE TABLE Lawyer (
  LawyerID    INT AUTO_INCREMENT PRIMARY KEY,
  Name        VARCHAR(255),
  Age         INT,
  PhoneNumber VARCHAR(20) UNIQUE,
  FaxNumber   VARCHAR(20) UNIQUE
) ENGINE=InnoDB;

-- 6) Inmates
CREATE TABLE Inmate (
  InmateID         INT AUTO_INCREMENT PRIMARY KEY,
  Name             VARCHAR(255),
  Age              INT,
  CrimeCommitted   VARCHAR(255),
  SentenceDuration INT,
  CellAssignment   INT,
  GuardID          INT,
  StaffID          INT,
  LawyerID         INT,
  RehabID          INT,
  BehaviorRecord   TEXT,

  FOREIGN KEY (CellAssignment) REFERENCES Cell(CellID),
  FOREIGN KEY (GuardID)        REFERENCES Guard(GuardID),
  FOREIGN KEY (StaffID)        REFERENCES Staff(StaffID),
  FOREIGN KEY (LawyerID)       REFERENCES Lawyer(LawyerID),
  FOREIGN KEY (RehabID)        REFERENCES Rehab(RehabID)
) ENGINE=InnoDB;

-- 7) Visitors (now Inmate exists)
CREATE TABLE Visitor (
  VisitorID            INT AUTO_INCREMENT PRIMARY KEY,
  Name                 VARCHAR(255),
  RelationshipToInmate VARCHAR(255),
  InmateID             INT,
  FOREIGN KEY (InmateID) REFERENCES Inmate(InmateID)
) ENGINE=InnoDB;
