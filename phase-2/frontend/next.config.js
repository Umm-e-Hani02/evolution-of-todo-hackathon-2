/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Enable experimental features for better Vercel deployment
  experimental: {
    // Support for output standalone for containerized deployments
    outputStandalone: true,
  },
  // Optimize for Vercel deployment
  swcMinify: true,
};

module.exports = nextConfig;
