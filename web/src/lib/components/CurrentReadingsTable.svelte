<script lang="ts">
	import type { CurrentReadings } from '$lib/types';

	let { readings }: { readings: CurrentReadings } = $props();

	const locations = ['Attic', 'Garage', 'Inside', 'Outside', 'HVAC'];
</script>

<div class="table-wrap">
	<h2>Current Readings</h2>
	<table>
		<thead>
			<tr>
				<th>Location</th>
				<th>Temperature</th>
				<th>Heat Index</th>
				<th>Humidity</th>
				<th>Pressure</th>
			</tr>
		</thead>
		<tbody>
			{#each locations as location (location)}
				{@const row = readings[location]}
				<tr>
					<td>{location}</td>
					<td>{row?.temperature_f ?? '—'}</td>
					<td>{row?.heat_index_f ?? '—'}</td>
					<td>{row?.humidity_pct ?? '—'}</td>
					<td>{row?.pressure_inHg ?? '—'}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</div>
