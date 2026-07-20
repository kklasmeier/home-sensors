export const ENV_LOCATIONS = ['Attic', 'Garage', 'Inside', 'Outside', 'HVAC'] as const;

export type EnvLocation = (typeof ENV_LOCATIONS)[number];

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

export const SYSTEM_ROUTES = [
	{ slug: 'garage-doors', label: 'Garage Doors', statusKey: 'Garagedoor' },
	{ slug: 'sump-pump', label: 'Sump Pump', statusKey: 'SumpPump' },
	{ slug: 'hvac', label: 'HVAC Cycles', statusKey: 'HVAC' }
] as const;

export function locationPath(location: string): string {
	return `/locations/${encodeURIComponent(location)}`;
}

export function systemPath(slug: string): string {
	return `/systems/${slug}`;
}

export function isEnvLocation(value: string): value is EnvLocation {
	return (ENV_LOCATIONS as readonly string[]).includes(value);
}
