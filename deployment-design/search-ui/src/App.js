import './App.css';


import React from "react";
import "@elastic/eui/dist/eui_theme_light.css";

import ElasticSearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  Paging,
  PagingInfo,
  Results,
  ResultsPerPage,
  SearchProvider,
  SearchBox,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import {
  Layout,
} from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

const connector = new ElasticSearchAPIConnector({
    host: process.env.REACT_ELASTICSEARCH_HOST || "http://localhost:9200",
    index: process.env.REACT_ELASTICSEARCH_INDEX || "cv-transcriptions",
//   apiKey:
//     process.env.REACT_ELASTICSEARCH_API_KEY ||
//     "SlUzdWE0QUJmN3VmYVF2Q0F6c0I6TklyWHFIZ3lTbHF6Yzc2eEtyeWFNdw=="
    connectionOptions: {
      // Optional connection options. TODO disable in production
      "Access-Control-Allow-Origin": "*", // Required for CORS support to work
      "Access-Control-Allow-Credentials": true, // Required for cookies, authorization headers with HTTPS
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, HEAD",
      "Access-Control-Allow-Headers": "Accept, Access-Control-Allow-Headers, Authorization, Content-Type, Cache-Control, Origin, Pragma, X-Requested-With",
      }
    }
);

const config = {
  debug: true,
  alwaysSearchOnInitialLoad: true,
  apiConnector: connector,
  hasA11yNotifications: true,
  searchQuery: {
    filters: [],
    search_fields: {
      generated_text: {},
      duration: {},
      age: {},
      gender: {},
      accent: {},
    },
    result_fields: {
      filename: { raw: {} },
      up_votes: { raw: {} },
      down_votes: { raw: {} },
      generated_text: {
        snippet: {
          size: 100,
          fallback: true
        }
      },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} },
      duration: { raw: {} },
    },
  },
    disjunctiveFacets: [
      "filename.keyword",
      "states.keyword",
      "date_established",
      "location"
    ],
    facets: {
      up_votes: {
        type: "range",
        ranges: [
          { from: 0, to: 50, name: "0 - 50" },
          { from: 51, to: 100, name: "51 - 100" },
          { from: 101, to: 200, name: "101 - 200" },
          { from: 201, name: "200+" }
        ]
      },
      down_votes: {
        type: "range",
        ranges: [
          { from: 0, to: 50, name: "0 - 50" },
          { from: 51, to: 100, name: "51 - 100" },
          { from: 101, to: 200, name: "101 - 200" },
          { from: 201, name: "200+" }
        ]
      },
      "age.keyword": { type: "range" },
      "gender.keyword": { type: "gender" },
      "accent.keyword": { type: "gender" },
    },
  autocompleteQuery: {
    results: {
      search_fields: {
        generated_text: {}
      },
      resultsPerPage: 5,
      result_fields: {
        title: {
          snippet: {
            size: 100,
            fallback: true
          }
        },
      }
    },
    suggestions: {
      types: {
        documents: {
          fields: ["filename"]
        }
      },
      size: 4
    }
  },
};

const SORT_OPTIONS = [
  {
    name: "filename",
    value: []
  },
  {
    name: "up_votes",
    value: [
      {
        field: "up_votes",
        direction: "desc"
      }
    ]
  },
  {
    name: "down_votes",
    value: [
      {
        field: "down_votes",
        direction: "desc"
      }
    ]
  },
];

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch
        mapContextToProps={({ wasSearched }) => ({
          wasSearched
        })}
      >
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={
                    <SearchBox
                      autocompleteMinimumCharacters={3}
                      autocompleteResults={{
                        linkTarget: "_blank",
                        sectionTitle: "Results",
                        titleField: "title",
                        shouldTrackClickThrough: true,
                        clickThroughTags: ["test"]
                      }}
                      autocompleteSuggestions={true}
                      debounceLength={0}
                    />
                  }
                  sideContent={
                    <div>
                       {wasSearched && (
                         <Sorting label={"Sort by"} sortOptions={SORT_OPTIONS} />
                       )}
                      <Facet
                        field="up_votes"
                        label="up_votes"
                        filterType="any"
                        isFilterable={true}
                      />
                      <Facet
                        field="down_votes"
                        label="down_votes"
                        filterType="any"
                        isFilterable={true}
                      />
                      <Facet
                        field="age.keyword"
                        label="age"
                        filterType="any"
                        isFilterable={true}
                      />
                      <Facet
                        field="gender.keyword"
                        label="gender"
                        filterType="any"
                        isFilterable={true}
                      />
                      <Facet
                        field="accent.keyword"
                        label="accent"
                        filterType="any"
                        isFilterable={true}
                      />
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField="filename"
                      shouldTrackClickThrough={true}
                      />}
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}