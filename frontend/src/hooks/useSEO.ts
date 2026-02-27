import { useEffect } from 'react';

interface SEOProps {
    title: string;
    description: string;
    keywords?: string;
    canonical?: string;
}

export const useSEO = ({ title, description, keywords, canonical }: SEOProps) => {
    useEffect(() => {
        document.title = title;

        const setMetaTag = (name: string, content: string) => {
            let element = document.querySelector(`meta[name="${name}"]`);
            if (!element) {
                element = document.createElement('meta');
                element.setAttribute('name', name);
                document.head.appendChild(element);
            }
            element.setAttribute('content', content);
        };

        const setOgTag = (property: string, content: string) => {
            let element = document.querySelector(`meta[property="${property}"]`);
            if (!element) {
                element = document.createElement('meta');
                element.setAttribute('property', property);
                document.head.appendChild(element);
            }
            element.setAttribute('content', content);
        };

        const setCanonicalLink = (href: string) => {
            let element = document.querySelector(`link[rel="canonical"]`);
            if (!element) {
                element = document.createElement('link');
                element.setAttribute('rel', 'canonical');
                document.head.appendChild(element);
            }
            element.setAttribute('href', href);
        };

        setMetaTag('description', description);
        setOgTag('og:title', title);
        setOgTag('og:description', description);
        setMetaTag('twitter:title', title);
        setMetaTag('twitter:description', description);

        if (keywords) {
            setMetaTag('keywords', keywords);
        }

        if (canonical) {
            setCanonicalLink(canonical);
            setOgTag('og:url', canonical);
        }

    }, [title, description, keywords, canonical]);
};
