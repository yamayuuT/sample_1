import React from 'react';
import { Container, Typography, TextField, Button, Box } from '@mui/material';
import styled from 'styled-components';



const Section = styled.section`
  padding: 60px 0;
  text-align: center;
`;

const Contact = () => {
  return (


    <Section id="contact">
      <Container maxWidth="sm">
        <Typography variant="h2" gutterBottom>
          お問い合わせ
        </Typography>
        <Box component="form" mt={3}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="お名前"
            autoFocus
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="メールアドレス"
            type="email"
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="お問い合わせ内容"
            multiline
            rows={4}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 3 }}
          >

            送信
          </Button>
        </Box>
      </Container>
    </Section>

  );
};


export default Contact;
