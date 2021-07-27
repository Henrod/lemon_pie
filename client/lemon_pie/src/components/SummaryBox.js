import { Grid, Paper, Typography, Box } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import nick from "../assets/nick.jpeg";

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(2),
    textAlign: "center",
    flexGrow: 1,
    margin: theme.spacing(2),
  },
  gridContainer: {
    spacing: 4,
    direction: "row",
    justify: "center",
  },
  gridItem: {
    fontSize: "63px",
  },
  photo: {
    height: "100px",
    width: "100px",
    marginLeft: theme.spacing(12),
  },
  profileName: {
    marginRight: theme.spacing(20),
  },
}));

const SummaryBox = ({ user, votes }) => {
  const classes = useStyles();

  return (
    <Paper key={user.key} className={classes.paper}>
      <Box display="flex" alignItems="center" justifyContent="center">
        <img src={nick} alt="profile" className={classes.photo} />
        <Box width="100%">
          <Typography variant="h4" className={classes.profileName}>
            {user.name}
          </Typography>
        </Box>
      </Box>
      <Grid container key={user.key} className={classes.gridContainer}>
        {Object.keys(votes).map((emojiKey) => (
          <Grid key={emojiKey} item lg={3} md={4} sm={6} xs={12}>
            <Box className={classes.gridItem}>
              {`${votes[emojiKey]["value"]} ${votes[emojiKey]["count"]}`}
            </Box>
          </Grid>
        ))}
      </Grid>
    </Paper>
  );
};

export default SummaryBox;
