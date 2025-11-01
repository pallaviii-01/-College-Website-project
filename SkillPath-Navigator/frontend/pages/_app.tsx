import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import { useEffect } from 'react';
import Head from 'next/head';

export default function App({ Component, pageProps }: AppProps) {
  useEffect(() => {
    document.documentElement.lang = 'en';
  }, []);

  return (
    <>
      <Head>
        <title>SkillPath Navigator - AI-Powered Learning Path Generator</title>
        <meta name="description" content="Personalized vocational training pathways aligned with NSQF" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}
