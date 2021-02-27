import { LinkButton, TopBar } from "../components";
import {
  ThemeProvider,
  createMuiTheme,
  Typography,
  Box,
} from "@material-ui/core";
import notFound from "../assets/notFound.gif";
import { makeStyles } from "@material-ui/core/styles";

const theme = createMuiTheme({});

const useStyles = makeStyles((theme) => ({
  image: {
    marginLeft: "auto",
    marginRight: "auto",
    display: "box",
  },
}));

const NotFound = () => {
  const classes = useStyles();
  return (
    <ThemeProvider theme={theme}>
      <TopBar />
      <Box>
        <Typography variant="h3" align="center">
          404 - Page Not Found 😞
        </Typography>
        <img src={notFound} alt="not found" className={classes.image} />
        <LinkButton
          to="/"
          text="Home"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          Home
        </LinkButton>
      </Box>
    </ThemeProvider>
  );
};

export default NotFound;
