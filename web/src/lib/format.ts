/** Format seconds since last reading (legacy sensorStatus.php display). */
export function formatSensorAge(seconds: number): string {
	const hours = Math.floor(seconds / 3600);
	const minutes = Math.floor((seconds % 3600) / 60);
	const secs = seconds % 60;

	let timeString = '';
	if (hours > 0) {
		timeString += `${hours.toString().padStart(2, '0')}:`;
	}
	if (hours > 0) {
		timeString += `${minutes.toString().padStart(2, '0')}:`;
	} else if (minutes > 0 || (minutes === 0 && hours === 0)) {
		timeString += `${minutes}:`;
	}
	timeString += secs.toString().padStart(2, '0');
	return timeString;
}

export function displayLocationName(location: string): string {
	if (location === 'SumpPump') return 'Sump Pump';
	if (location === 'Garagedoor') return 'Garagedoor';
	return location;
}

export function parseApiDate(value: string): Date {
	return new Date(value.replace(' ', 'T'));
}

export function formatChartLabel(value: string): string {
	const d = parseApiDate(value);
	return d.toLocaleString(undefined, {
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: '2-digit'
	});
}
