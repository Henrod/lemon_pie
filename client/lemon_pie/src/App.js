import "./App.css";
import { Vote, NotFound, Summary, Login, Total } from "./pages";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
  const buildPages = (pages) => (
    <Router className="App">
      <div>
        <Switch>
          {pages.map((page) => (
            <Route exact path={page.path} key={page.path}>
              {page.page}
            </Route>
          ))}
          <Route>
            <NotFound />
          </Route>
        </Switch>
      </div>
    </Router>
  );

  return buildPages([
    {
      path: "/",
      page: <Summary />,
    },
    {
      path: "/votes",
      page: <Vote />,
    },
    {
      path: "/login",
      page: <Login />,
    },
    {
      path: "/total",
      page: <Total />,
    },
  ]);
}

export default App;
