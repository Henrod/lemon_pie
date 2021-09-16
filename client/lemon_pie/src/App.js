import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
} from "react-router-dom";
import "./App.css";
import { Login, Summary, Total, Vote } from "./pages";

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
          <Redirect to="/" />
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
