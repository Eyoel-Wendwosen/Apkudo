CREATE TABLE FaultType (
    id character varying(25) PRIMARY KEY,
    fault_code integer,
    fault_description character varying(255)
);

CREATE TABLE EventType (
    id character varying(25) PRIMARY KEY,
    event_type integer,
    event_name character varying(255)
);


CREATE TABLE Record (
    id character varying(25) PRIMARY KEY,
    event_type_id character varying(25) REFERENCES EventType(id),
    IMIE character varying(255),
    SKU character varying(255)
);


CREATE TABLE DeviceFault (
    id character varying(255) PRIMARY KEY,
    fault_type_id character varying(25) REFERENCES FaultType(id),
    record_id character varying(25) REFERENCES Record(id)
);

