export const ENV_LOCATIONS = ['Attic', 'Garage', 'Inside', 'Outside', 'HVAC'] as const;

export const STATUS_TILES = [
	'Attic',
	'Garage',
	'Inside',
	'Outside',
	'Garagedoor',
	'SumpPump',
	'HVAC'
] as const;

export const SUMMARY_LOCATIONS = ['Garage', 'Inside', 'Outside', 'Attic', 'HVAC'] as const;

export const REFRESH_MS = 60_000;

export const CHART_COLORS: Record<string, string> = {
	Attic: '#4fc3f7',
	Garage: '#ffb74d',
	Inside: '#81c784',
	Outside: '#9575cd',
	HVAC: '#f06292'
};
