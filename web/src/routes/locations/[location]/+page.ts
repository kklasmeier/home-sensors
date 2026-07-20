import { ENV_LOCATIONS } from '$lib/constants';

export function entries() {
	return ENV_LOCATIONS.map((location) => ({ location }));
}
