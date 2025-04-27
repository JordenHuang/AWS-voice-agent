/** @type {import('next').NextConfig} */
const nextConfig = {
  // basePath: '/ai-agent',
  // output: 'export',
  output: 'standalone',
  reactStrictMode: false,
  webpack(config) {
    // // Grab the existing rule that handles SVG imports
    // const fileLoaderRule = config.module.rules.find((rule) =>
    //   rule.test?.test?.('.svg'),
    // )

    // config.module.rules.push(
    //   // Reapply the existing rule, but only for svg imports ending in ?url
    //   {
    //     ...fileLoaderRule,
    //     test: /\.svg$/i,
    //     resourceQuery: /url/, // *.svg?url
    //   },
    //   // Convert all other *.svg imports to React components
    //   {
    //     test: /\.svg$/i,
    //     issuer: fileLoaderRule.issuer,
    //     resourceQuery: { not: [...fileLoaderRule.resourceQuery.not, /url/] }, // exclude if *.svg?url
    //     use: ['@svgr/webpack'],
    //   },
    // )

    // // Modify the file loader rule to ignore *.svg, since we have it handled now.
    // fileLoaderRule.exclude = /\.svg$/i
    config.module.rules.push({
      test: /\.svg$/,
      issuer: /\.[jt]sx?$/, // Only apply svgr to JS/TS files
      use: [
        {
          loader: '@svgr/webpack',
          options: {
            // svgr options here if you want
            icon: true,
          },
        },
      ],
    });
    return config;
  }
};

export default nextConfig;
