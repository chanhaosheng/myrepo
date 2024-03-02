import './App.css';


import React from "react";
import "@elastic/eui/dist/eui_theme_light.css";

import ElasticSearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
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
      // Optional connection options.
      "Access-Control-Allow-Headers": "Accept, Access-Control-Allow-Headers, Authorization, Content-Type"
      }
    }
);

const config = {
  debug: true,
  alwaysSearchOnInitialLoad: true,
  apiConnector: connector,
  hasA11yNotifications: true,
  searchQuery: {
    search_fields: {
      generated_text: {},
      duration: {},
      age: {},
      gender: {},
      accent: {},
    },
    result_fields: {
      filename: { raw: {} },
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
};


export default function App() {
  return (
    <div>
      <SearchProvider config={config}>
        <WithSearch mapContextToProps={({ results, searchTerm, setSearchTerm }) => ({ results, searchTerm, setSearchTerm })}>
          {({ results, searchTerm, setSearchTerm }) => (
            <div className="App">
              <Layout
                header={<SearchBox searchTerm={searchTerm} setSearchTerm={setSearchTerm} />}
                bodyContent={<Results results={results} titleField="filename" />}
                bodyFooter={<Paging />}
              />
            </div>
          )}
        </WithSearch>
      </SearchProvider>
    </div>
  );
}


// export default function App() {
//   return (
//     <div className="App">
//       <h1>Hello world!</h1>
//     </div>
//   );
// }
