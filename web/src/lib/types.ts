export type SensorStatus = {
	location: string;
	status: 'Green' | 'Yellow' | 'Red';
	diff_seconds: number;
};

export type CurrentReading = {
	temperature_f: string;
	heat_index_f: string;
	humidity_pct: string;
	pressure_inHg: string;
} | null;

export type CurrentReadings = Record<string, CurrentReading>;

export type ChartRow = {
	reading_dttm: string;
	location?: string;
	temperature_f?: string;
	heat_index_f?: string;
	humidity_pct?: string;
	pressure_inHg?: string;
	water_level?: string;
};

export type GarageDoor = {
	label: string;
	column: string;
	status: string;
	image: string;
	duration: string;
};

export type GarageChartRow = {
	reading_dttm: string;
	mainGarageDoor: number;
	thirdCarDoor: number;
};

export type SumpCycleRow = {
	reading_date: string;
	num_cycles: string;
};

export type HvacCycleRow = {
	cycle_date: string;
	cycle_count: number;
};

export type SummaryData = Record<string, Record<string, string>>;
