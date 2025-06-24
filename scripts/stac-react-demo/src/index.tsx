import './style.scss';

import ReactDOM from "react-dom/client";
import { PageHeader, PageFooter } from "./components/BCGovComponents";
import App from "./App";

const headerElement = document.getElementById("header");
const appElement = document.getElementById("app"); 
const footerElement = document.getElementById("footer");

if (headerElement) {
  ReactDOM.createRoot(headerElement).render(<PageHeader />);
}

if (appElement) {
  ReactDOM.createRoot(appElement).render(<App />);
}

if (footerElement) {
  ReactDOM.createRoot(footerElement).render(<PageFooter />);
}
