import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  photo: {
    height: undefined,
    width: "200px",
    aspectRatio: "1",
    marginLeft: theme.spacing(12),
    marginBottom: theme.spacing(2),
  },
}));

const REACT_APP_OBJECT_STORAGE_URL = process.env.REACT_APP_OBJECT_STORAGE_URL;

const ProfilePhoto = ({ user }) => {
  const classes = useStyles();
  const photoURL = `${REACT_APP_OBJECT_STORAGE_URL}/${user.key}.jpg`;
  return <img src={photoURL} alt="profile" className={classes.photo} />;
};

export default ProfilePhoto;
