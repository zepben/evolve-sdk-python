const path = require("path");
const versions = require("./versions.json");

module.exports = {
  title: "Evolve SDK (Python)",
  tagline: "",
  url: "https://zepben.github.io/evolve/sdk-jvm/",
  baseUrl: "/evolve/docs/python-sdk/",
  onBrokenLinks: "warn",
  favicon: "img/favicon.ico",
  organizationName: "zepben",
  projectName: "evolve-sdk-python",
  themeConfig: {
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      logo: {
        alt: "Zepben",
        src: "img/logo.svg",
        srcDark: "img/logo-dark.svg",
        href: "https://www.zepben.com/",
      },
      items: [
        {
          to: "https://zepben.github.io/evolve/docs",
          label: "Evolve",
          position: "left",
        },
        {
          to: "/",
          activeBasePath: "docs",
          label: "Docs",
          position: "left",
        },
        {
          to: "release-notes",
          activeBasePath: "release-notes",
          label: "Release Notes",
          position: "right",
        },
        {
          type: "docsVersionDropdown",
          position: "right",
        },
        {
          href: "https://github.com/zepben/evolve-sdk-jvm/",
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },
      ],
    },
    footer: {
      style: "dark",
      links: [],
      copyright: `Copyright © ${new Date().getFullYear()} Zeppelin Bend Pty. Ltd.`,
    },
    googleAnalytics: {
      trackingID: "UA-81287323-1",
      anonymizeIP: false,
    },
    algolia: {
      apiKey: "bd9b85d42d37ebf66b352f07513f4d6a",
      indexName: "python-sdk-docs",
      appId: "IU0L20J0JX"
    },
  },
  presets: [
    [
      "@zepben/docusaurus-preset",
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl: "https://github.com/zepben",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
};
