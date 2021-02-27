import {
  AppBar,
  Toolbar,
  Typography,
  ThemeProvider,
  createMuiTheme,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  appBar: {
    alignItems: "center",
    position: "sticky",
  },
}));

const theme = createMuiTheme({});

const TopBar = () => {
  const classes = useStyles();
  return (
    <ThemeProvider theme={theme}>
      <AppBar color="inherit" className={classes.appBar}>
        <Toolbar>
          <Typography variant="h2">
            {process.env.REACT_APP_TITLE || "Lemon Pie"}
          </Typography>
        </Toolbar>
      </AppBar>
    </ThemeProvider>
  );
};

export default TopBar;
