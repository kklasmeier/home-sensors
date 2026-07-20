import { SYSTEM_ROUTES } from './constants';

export type Breadcrumb = {
	label: string;
	href?: string;
};

const SYSTEM_LABELS = Object.fromEntries(SYSTEM_ROUTES.map((s) => [s.slug, s.label]));

/** Build breadcrumb trail from the current URL pathname. */
export function breadcrumbsForPath(pathname: string): Breadcrumb[] {
	const path = pathname.replace(/\/$/, '') || '/';

	if (path === '/') {
		return [{ label: 'Home' }];
	}

	const crumbs: Breadcrumb[] = [{ label: 'Home', href: '/' }];

	if (path === '/logs') {
		crumbs.push({ label: 'Collector Logs' });
		return crumbs;
	}

	if (path.startsWith('/locations/')) {
		const location = decodeURIComponent(path.slice('/locations/'.length));
		crumbs.push({ label: location || 'Location' });
		return crumbs;
	}

	if (path.startsWith('/systems/')) {
		const slug = path.slice('/systems/'.length).split('/')[0];
		crumbs.push({ label: SYSTEM_LABELS[slug] ?? slug });
		return crumbs;
	}

	crumbs.push({ label: 'Page' });
	return crumbs;
}
