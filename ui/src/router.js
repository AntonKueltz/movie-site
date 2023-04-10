import { createBrowserRouter } from "react-router-dom";
import Grid from '@mui/material/Grid';

import MovieDetail from "./MovieDetail";
import MovieList from "./MovieList";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Grid container spacing={2}><MovieList /></Grid>
    },
    {
        path: "/movie/:movieId",
        element: <MovieDetail  />
    },
]);