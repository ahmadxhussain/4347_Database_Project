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

-- 6) Inmates (holds the one-to-many and the old “StaffID/LawyerID/RehabID” columns
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

-- ─── Junction tables for the 3 many-to-many relationships ─────────────────────

-- Inmates ⇄ Rehabilitation Programs
CREATE TABLE Inmate_RehabProgram (
  InmateID        INT       NOT NULL,
  RehabID         INT       NOT NULL,
  EnrollDate      DATE      NOT NULL,
  CompletionDate  DATE      NULL,
  Outcome         VARCHAR(50),
  PRIMARY KEY    (InmateID, RehabID),
  FOREIGN KEY (InmateID) REFERENCES Inmate(InmateID),
  FOREIGN KEY (RehabID)  REFERENCES Rehab(RehabID)
) ENGINE=InnoDB;

-- Inmates ⇄ Staff
CREATE TABLE Inmate_Staff (
  InmateID         INT       NOT NULL,
  StaffID          INT       NOT NULL,
  AssignmentStart  DATE      NOT NULL,
  AssignmentEnd    DATE      NULL,
  PRIMARY KEY    (InmateID, StaffID, AssignmentStart),
  FOREIGN KEY (InmateID) REFERENCES Inmate(InmateID),
  FOREIGN KEY (StaffID)  REFERENCES Staff(StaffID)
) ENGINE=InnoDB;

-- Inmates ⇄ Lawyers
CREATE TABLE Inmate_Lawyer (
  InmateID       INT          NOT NULL,
  LawyerID       INT          NOT NULL,
  CaseStartDate  DATE         NOT NULL,
  CaseOutcome    VARCHAR(50),
  PRIMARY KEY    (InmateID, LawyerID, CaseStartDate),
  FOREIGN KEY (InmateID) REFERENCES Inmate(InmateID),
  FOREIGN KEY (LawyerID) REFERENCES Lawyer(LawyerID)
) ENGINE=InnoDB;
