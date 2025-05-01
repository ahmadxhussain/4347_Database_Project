DROP DATABASE IF EXISTS PrisonManagement;
CREATE DATABASE PrisonManagement;
USE PrisonManagement;

-- 1) Guards
CREATE TABLE Guard (
  GuardID        INT AUTO_INCREMENT PRIMARY KEY,
  Name           VARCHAR(255)       NOT NULL,
  `Rank`         VARCHAR(50),
  ShiftSchedule  VARCHAR(255)
) ENGINE=InnoDB;

-- 2) Cells (each cell has one guard in charge)
CREATE TABLE Cell (
  CellID         INT AUTO_INCREMENT PRIMARY KEY,
  BlockNumber    VARCHAR(50)       NOT NULL,
  MaxOccupancy   INT               NOT NULL,
  SecurityLevel  VARCHAR(50)       NOT NULL,
  GuardInCharge  INT,
  FOREIGN KEY (GuardInCharge) REFERENCES Guard(GuardID)
) ENGINE=InnoDB;

-- 3) Rehabilitation programs
CREATE TABLE Rehab (
  RehabID        INT AUTO_INCREMENT PRIMARY KEY,
  Name           VARCHAR(255)       NOT NULL,
  Type           VARCHAR(100),
  Therapy        VARCHAR(100),
  JobTraining    VARCHAR(100),
  SuccessRate    FLOAT
) ENGINE=InnoDB;

-- 4) Staff (each staff can have one roommate—a self–FK)
CREATE TABLE Staff (
  StaffID        INT AUTO_INCREMENT PRIMARY KEY,
  Name           VARCHAR(255)       NOT NULL,
  Role           VARCHAR(100),
  Department     VARCHAR(100),
  StaffType      ENUM('Guard','Doctor','EducationProfessional'),
  RoommateID     INT,
  FOREIGN KEY (RoommateID) REFERENCES Staff(StaffID)
) ENGINE=InnoDB;

-- 5) Lawyers
CREATE TABLE Lawyer (
  LawyerID       INT AUTO_INCREMENT PRIMARY KEY,
  Name           VARCHAR(255)       NOT NULL,
  Age            INT,
  PhoneNumber    VARCHAR(20) UNIQUE,
  FaxNumber      VARCHAR(20) UNIQUE
) ENGINE=InnoDB;

-- 6) Inmates (all “many” links point here)
CREATE TABLE Inmate (
  InmateID         INT AUTO_INCREMENT PRIMARY KEY,
  Name             VARCHAR(255)       NOT NULL,
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

-- 7) Visitors (each visitor record belongs to one inmate)
CREATE TABLE Visitor (
  VisitorID            INT AUTO_INCREMENT PRIMARY KEY,
  Name                 VARCHAR(255)       NOT NULL,
  RelationshipToInmate VARCHAR(255),
  InmateID             INT,
  FOREIGN KEY (InmateID) REFERENCES Inmate(InmateID)
) ENGINE=InnoDB;
