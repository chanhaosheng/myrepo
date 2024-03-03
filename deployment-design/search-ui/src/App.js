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
    index: process.env.REACT_ELASTICSEARCH_INDEX || "cv-transcriptions"
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
      text: {
        snippet: {
          size: 100,
          fallback: true
        }
      },
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
      "gender.keyword"
    ],
    facets: {
      "age.keyword": { type: "value" },
      "gender.keyword": { type: "value" },
      "accent.keyword": { type: "value" },
    },
  autocompleteQuery: {
    results: {
      search_fields: {
        generated_text: {},
        duration: {},
        age: {},
        gender: {},
        accent: {},
      },
      resultsPerPage: 5,
      result_fields: {
        generated_text: {
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
          fields: ["generated_text", "age", "gender", "accent"]
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
                        titleField: "filename",
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
                        field="age.keyword"
                        label="Age"
                        filterType="any"
                      />
                      <Facet
                        field="gender.keyword"
                        label="Gender"
                        filterType="any"
                      />
                      <Facet
                        field="accent.keyword"
                        label="Accent"
                        filterType="any"
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