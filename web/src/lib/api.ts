import { ENV_LOCATIONS } from './constants';
import type {
	ChartRow,
	CurrentReadings,
	GarageChartRow,
	GarageDoor,
	HvacCycleRow,
	SensorStatus,
	SumpCycleRow,
	SummaryData
} from './types';

const API_BASE = import.meta.env.VITE_API_BASE ?? '';

async function getJson<T>(path: string): Promise<T> {
	const response = await fetch(`${API_BASE}${path}`);
	if (!response.ok) {
		throw new Error(`${path} failed: ${response.status}`);
	}
	return response.json() as Promise<T>;
}

async function getText(path: string): Promise<string> {
	const response = await fetch(`${API_BASE}${path}`);
	if (!response.ok) {
		throw new Error(`${path} failed: ${response.status}`);
	}
	return response.text();
}

export function getSensorStatus(): Promise<SensorStatus[]> {
	return getJson('/api/v1/sensors/status');
}

export function getCurrentReadings(): Promise<CurrentReadings> {
	return getJson('/api/v1/sensors/current');
}

export function getGarageStatus(): Promise<{ doors: GarageDoor[] }> {
	return getJson('/api/v1/garage/status');
}

export function getGarageCharts(): Promise<GarageChartRow[]> {
	return getJson('/api/v1/garage/charts');
}

export function getSumpPumpCharts(): Promise<ChartRow[]> {
	return getJson('/api/v1/sump-pump/charts');
}

export function getSumpPumpCycles(): Promise<SumpCycleRow[]> {
	return getJson('/api/v1/sump-pump/cycles');
}

export function getHvacCycles(): Promise<HvacCycleRow[]> {
	return getJson('/api/v1/hvac/cycles');
}

export function getLocationSummary(location: string): Promise<SummaryData> {
	return getJson(`/api/v1/sensors/${location}/summary`);
}

export function getCollectLogs(): Promise<string> {
	return getText('/api/v1/logs/collect');
}

export async function getLocationCharts(location: string): Promise<ChartRow[]> {
	return getJson(`/api/v1/sensors/${location}/charts`);
}

export async function getAllLocationCharts(): Promise<ChartRow[]> {
	const chunks = await Promise.all(ENV_LOCATIONS.map((loc) => getLocationCharts(loc)));
	return chunks.flat();
}

export async function getAllSummaries(): Promise<Record<string, SummaryData>> {
	const entries = await Promise.all(
		ENV_LOCATIONS.map(async (location) => [location, await getLocationSummary(location)] as const)
	);
	return Object.fromEntries(entries);
}
