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
