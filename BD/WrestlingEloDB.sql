DROP TABLE IF EXISTS HasOrganisedEvent;
DROP TABLE IF EXISTS SoloInMatch;
DROP TABLE IF EXISTS TagInMatch;
DROP TABLE IF EXISTS StableInMatch;
DROP TABLE IF EXISTS HasTitleSolo;
DROP TABLE IF EXISTS HasTitleTag;
DROP TABLE IF EXISTS HasTitleStable;
DROP TABLE IF EXISTS IsPartFederationWrestler;
DROP TABLE IF EXISTS IsPartFederationTag;
DROP TABLE IF EXISTS IsPartFederationStable;
DROP TABLE IF EXISTS IsPartTag;
DROP TABLE IF EXISTS IsPartStable;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Titles;
DROP TABLE IF EXISTS Stables;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Wrestlers;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Federations;
DROP TABLE IF EXISTS Nationalities;

--create nationality table
CREATE TABLE Nationalities (
	NationalityID INT IDENTITY(1,1) PRIMARY KEY,
	NationalityName NVARCHAR(255)
);

--create federation table
CREATE TABLE Federations (
	FederationID INT IDENTITY(1,1) PRIMARY KEY,
	FederationName NVARCHAR(255) NOT NULL,
	FederationAcronym NVARCHAR(5) NOT NULL,
	FederationNationalityID INT,
	FederationActive BIT
	FOREIGN KEY (FederationNationalityID) REFERENCES Nationalities(NationalityID)
);

CREATE TABLE Events (
	EventID INT IDENTITY(1,1) PRIMARY KEY,
	EventName NVARCHAR(255),
	EventCountryID INT,
	EventDate DATETIME,
	EventCagematchRating FLOAT,
	FOREIGN KEY (EventCountryID) REFERENCES Nationalities(NationalityID)
)

--create wrestler table
CREATE TABLE Wrestlers (
	WrestlerID INT IDENTITY(1,1) PRIMARY KEY,
	WrestlerName NVARCHAR(255),
	WrestlerGender NVARCHAR(6),
	WrestlerNationalityID INT,
	WrestlerAlignment NVARCHAR(10),
	WrestlerFederationID INT,
	WrestlerActive BIT,
	WrestlerElo INT,
	WrestlerStartElo INT,
	WrestlerPeakElo INT,
	WrestlerWin INT,
	WrestlerTie INT,
	WrestlerLose INT,
	WrestlerCagematchRating FLOAT,
	WrestlerTheme NVARCHAR(255),
	FOREIGN KEY (WrestlerNationalityID) REFERENCES Nationalities(NationalityID),
	FOREIGN KEY (WrestlerFederationID) REFERENCES Federations(FederationID)
);

--create tag table
CREATE TABLE Tags (
	TagID INT IDENTITY(1,1) PRIMARY KEY,
	TagName NVARCHAR(255),
	TagNationalityID INT,
	TagAlignment NVARCHAR(10),
	TagFederationID INT,
	TagActive BIT,
	TagElo INT,
	TagStartElo INT,
	TagPeakElo INT,
	TagWin INT,
	TagTie INT,
	TagLose INT,
	TagCagematchRating FLOAT,
	TagTheme NVARCHAR(255),
	FOREIGN KEY (TagNationalityID) REFERENCES Nationalities(NationalityID),
	FOREIGN KEY (TagFederationID) REFERENCES Federations(FederationID)
);

--create stable table
CREATE TABLE Stables (
	StableID INT IDENTITY(1,1) PRIMARY KEY,
	StableName NVARCHAR(255),
	StableNationalityID INT,
	StableAlignment NVARCHAR(10),
	StableFederationID INT,
	StableActive BIT,
	StableWin INT,
	StableTie INT,
	StableLose INT,
	StableCagematchRating FLOAT,
	StableTheme NVARCHAR(255),
	FOREIGN KEY (StableNationalityID) REFERENCES Nationalities(NationalityID),
	FOREIGN KEY (StableFederationID) REFERENCES Federations(FederationID)
);

--create title table
CREATE TABLE Titles (
	TitleID INT IDENTITY(1,1) PRIMARY KEY,
	TitleName NVARCHAR(255),
	TitleFederation NVARCHAR(255),
	TitleType NVARCHAR(255),
	TitleActive BIT,
	TitlePrestige NVARCHAR(255)
);

--create match table
CREATE TABLE Matches (
	MatchID INT IDENTITY(1,1) PRIMARY KEY,
	MatchDate DATETIME,
	MatchType NVARCHAR(255),
	MatchWinner NVARCHAR(255),
	MatchLoser NVARCHAR(255),
	MatchStar FLOAT,
	MatchCagematch FLOAT
);

--create IsPartTag table
CREATE TABLE IsPartTag (
	WrestlerID INT,
	TagID INT,
	FOREIGN KEY (WrestlerID) REFERENCES Wrestlers(WrestlerID),
	FOREIGN KEY (TagID) REFERENCES Tags(TagID)
)

--create IsPartStable table
CREATE TABLE IsPartStable (
	WrestlerID INT,
	StableID INT,
	FOREIGN KEY (WrestlerID) REFERENCES Wrestlers(WrestlerID),
	FOREIGN KEY (StableID) REFERENCES Stables(StableID)
)

--create IsPartFederationWrestler table
CREATE TABLE IsPartFederationWrestler (
	WrestlerID INT,
	FederationID INT,
	FOREIGN KEY (WrestlerID) REFERENCES Wrestlers(WrestlerID),
	FOREIGN KEY (FederationID) REFERENCES Federations(FederationID)
)

--create IsPartFederationTag table
CREATE TABLE IsPartFederationTag (
	TagID INT,
	FederationID INT,
	FOREIGN KEY (TagID) REFERENCES Tags(TagID),
	FOREIGN KEY (FederationID) REFERENCES Federations(FederationID)
)

--create IsPartFederationStable table
CREATE TABLE IsPartFederationStable (
	StableID INT,
	FederationID INT,
	FOREIGN KEY (StableID) REFERENCES Stables(StableID),
	FOREIGN KEY (FederationID) REFERENCES Federations(FederationID)
)

--create HasTitleSolo table
CREATE TABLE HasTitleSolo (
	WrestlerID INT,
	TitleID INT,
	FOREIGN KEY (WrestlerID) REFERENCES Wrestlers(WrestlerID),
	FOREIGN KEY (TitleID) REFERENCES Titles(TitleID)
)

--create HasTitleTag table
CREATE TABLE HasTitleTag (
	TagID INT,
	TitleID INT,
	FOREIGN KEY (TagID) REFERENCES Tags(TagID),
	FOREIGN KEY (TitleID) REFERENCES Titles(TitleID)
)

--create HasTitleStable table
CREATE TABLE HasTitleStable (
	StableID INT,
	TitleID INT,
	FOREIGN KEY (StableID) REFERENCES Stables(StableID),
	FOREIGN KEY (TitleID) REFERENCES Titles(TitleID)
)

--create SoloInMatch table
CREATE TABLE SoloInMatch (
	WrestlerID INT,
	MatchID INT,
	TeamNumber INT,
	FOREIGN KEY (WrestlerID) REFERENCES Wrestlers(WrestlerID),
	FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
)

--create TagInMatch table
CREATE TABLE TagInMatch (
	TagID INT,
	MatchID INT,
	TeamNumber INT,
	FOREIGN KEY (TagID) REFERENCES Tags(TagID),
	FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
)

--create StableInMatch table
CREATE TABLE StableInMatch (
	StableID INT,
	MatchID INT,
	TeamNumber INT,
	FOREIGN KEY (StableID) REFERENCES Stables(StableID),
	FOREIGN KEY (MatchID) REFERENCES Matches(MatchID)
)

--create HasOrganisedEvent table
CREATE TABLE HasOrganisedEvent (
	EventID INT,
	FederationID INT,
	FOREIGN KEY (EventID) REFERENCES Events(EventID),
	FOREIGN KEY (FederationID) REFERENCES Federations(FederationID)
)