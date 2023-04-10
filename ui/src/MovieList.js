import { gql, useQuery } from '@apollo/client';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';

const GET_MOVIES = gql`
  query GetMovies {
    movies {
      id
      title
      year
      imgUrl
      avgRating
    }
  }
`;

export default function MovieList() {
    const { loading, error, data } = useQuery(GET_MOVIES);
  
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error : {error.message}</p>;
  
    return data.movies.map(({ id, title, year, imgUrl, avgRating }) => (
      <Grid item xs={3}>
        <Card sx={{ maxWidth: 270 }}>
          <CardActionArea href={`/movie/${id}`}>
            <CardMedia
              component="img"
              image={`${imgUrl}`}
              alt={`${title} Poster`}
            />
            <CardContent>
              <Typography variant="h5" component="div">
                {title}
              </Typography>
              <Typography variant="subtitle1">
                ({year})
              </Typography>
              <Typography sx={{ mb: 1.5 }} color="text.secondary">
                {avgRating}/10
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </Grid>
    ));
  }