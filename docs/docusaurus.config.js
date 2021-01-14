/*
 * Copyright 2021 Zeppelin Bend Pty Ltd
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const zepbenDocusaurusPreset = require("@zepben/docusaurus-preset");
const versions = require("./versions.json");

module.exports = {
  title: "Evolve SDK (Python)",
  tagline: "",
  url: "https://zepben.github.io/evolve/docs/python-sdk",
  baseUrl: "/evolve/docs/python-sdk/",
  onBrokenLinks: "warn",
  favicon: "img/favicon.ico",
  organizationName: "zepben",
  projectName: "evolve-sdk-python",
  themeConfig: {
    ...zepbenDocusaurusPreset.defaultThemeConfig,
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
    algolia: {
      ...zepbenDocusaurusPreset.defaultThemeConfig.algolia,
      searchParameters: {
        facetFilters: ["project:python-sdk"]
      }
    },
    metadatas: [{name: 'docsearch:project', content: 'python-sdk'}],
  },
  presets: [
    [
      "@zepben/docusaurus-preset",
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve("./sidebars.js"),
          versions: versions.reduce((acc, curr) => {
            acc[curr] = {label: curr, path: curr};
            return acc;
          }, {})
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],
};
