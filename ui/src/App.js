import { RouterProvider } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Link from '@mui/material/Link';
import Toolbar from '@mui/material/Toolbar';

import { router } from './router.js';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function NavBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Link href="/" color="inherit" variant="h5" sx={{ flexGrow: 1 }}>
            Shitty Movies
          </Link>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <NavBar />
      <Box sx={{ flexGrow: 1 }}>
      <RouterProvider router={router} />
      </Box>
    </ThemeProvider>
  );
}
