import type { ChartRow } from './types';
import { CHART_COLORS } from './constants';
import { formatChartLabel } from './format';

export type ChartDataset = {
	label: string;
	data: (number | null)[];
	borderColor: string;
};

export function buildMultiLocationChart(
	rows: ChartRow[],
	field: keyof ChartRow
): { labels: string[]; datasets: ChartDataset[] } {
	const byLocation: Record<string, Record<string, number>> = {};

	for (const row of rows) {
		const location = row.location;
		if (!location) continue;
		const value = row[field];
		if (value === undefined || value === null) continue;
		if (!byLocation[location]) byLocation[location] = {};
		byLocation[location][row.reading_dttm] = parseFloat(String(value));
	}

	const allTimes = [...new Set(rows.map((r) => r.reading_dttm))].sort();
	const labels = allTimes.map(formatChartLabel);
	const datasets = Object.keys(byLocation)
		.sort()
		.map((location) => ({
			label: location,
			borderColor: CHART_COLORS[location] ?? '#ffffff',
			data: allTimes.map((t) => byLocation[location][t] ?? null)
		}));

	return { labels, datasets };
}

export function buildSingleSeriesChart(
	rows: { reading_dttm: string; value: number }[],
	label: string,
	color = '#4fc3f7'
): { labels: string[]; datasets: ChartDataset[] } {
	return {
		labels: rows.map((r) => formatChartLabel(r.reading_dttm)),
		datasets: [
			{
				label,
				borderColor: color,
				data: rows.map((r) => r.value)
			}
		]
	};
}

export function buildBarChart(
	rows: { label: string; value: number }[],
	label: string,
	color = '#4fc3f7'
): { labels: string[]; datasets: ChartDataset[] } {
	return {
		labels: rows.map((r) => r.label),
		datasets: [
			{
				label,
				borderColor: color,
				data: rows.map((r) => r.value)
			}
		]
	};
}

function fieldValue(row: ChartRow, field: keyof ChartRow): number | null {
	const value = row[field];
	if (value === undefined || value === null) return null;
	return parseFloat(String(value));
}

/** Single-location line charts from one location's chart API response. */
export function buildLocationChartSet(rows: ChartRow[], location: string, color: string) {
	const series = (field: keyof ChartRow, label: string) =>
		buildSingleSeriesChart(
			rows
				.map((row) => {
					const value = fieldValue(row, field);
					return value === null ? null : { reading_dttm: row.reading_dttm, value };
				})
				.filter((row): row is { reading_dttm: string; value: number } => row !== null),
			label,
			color
		);

	return {
		temperature: series('temperature_f', 'Temperature'),
		heatIndex: series('heat_index_f', 'Heat Index'),
		humidity: series('humidity_pct', 'Humidity'),
		pressure: series('pressure_inHg', 'Pressure')
	};
}

export function buildGarageDoorChart(rows: import('./types').GarageChartRow[]) {
	return {
		labels: rows.map((r) => formatChartLabel(r.reading_dttm)),
		datasets: [
			{
				label: 'Main Garage Door',
				borderColor: '#4fc3f7',
				data: rows.map((r) => r.mainGarageDoor)
			},
			{
				label: '3rd Car Door',
				borderColor: '#ffb74d',
				data: rows.map((r) => r.thirdCarDoor)
			}
		]
	};
}
