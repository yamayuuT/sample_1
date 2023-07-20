// About.jsx

import React from 'react';
import { Box, Typography, Grid, List, ListItem, ListItemIcon, ListItemText, Divider, Card, CardContent, CardMedia } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import './About.css'; // CSSをインポート

const About = () => {
    return (
      <Box id="about" className="about-container">
        <Typography variant="h2" gutterBottom className="section-title">
            このアプリケーションについて
        </Typography>
        <Box className="card-container">
          <Card>
            <CardMedia
              className="card-media"
              image="images/your_image.jpg" // Set image path accordingly
              title="近似最適化とは？"
            />
            <CardContent>
              <Typography variant="h5" gutterBottom className="card-title">
                  近似最適化とは？
              </Typography>
              <Typography variant="body1" className="card-text">
                  近似最適化は、ある問題に対して最適な解を求める代わりに、「近似的に」最適な解を効率的に求める手法です。
                  一部の問題については、最適な解を直接求めることは現実的には困難であるため、近似最適化が有用となります。
              </Typography>
            </CardContent>
          </Card>
          <Card>
            <CardMedia
              className="card-media"
              image="images/your_image.jpg" // Set image path accordingly
              title="量子サンプラーとは？"
            />
            <CardContent>
              <Typography variant="h5" gutterBottom className="card-title">
                  量子サンプラーとは？
              </Typography>
              <Typography variant="body1" className="card-text">
                  量子サンプラーは、量子ビット（qubits）を利用して問題の解を「サンプリング」するデバイスです。量子状態の重ね合わせとエンタングルメントという量子力学の原理を利用して、問題の全ての可能性を同時に探索し、解を見つけ出します。これにより、一部の特定の問題に対しては、従来のコンピュータよりも高速に解を見つけることが可能です。
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box className="card-container">
          <Card>
            <CardMedia
              className="card-media"
              image="images/your_image.jpg" // Set image path accordingly
              title="このアプリケーションの利点"
            />
            <CardContent>
              <Typography variant="h5" gutterBottom className="card-title">
                  このアプリケーションの利点
              </Typography>
              <Typography variant="body1" className="card-text">
                  近似最適化と量子サンプリングの二つの手法を採用しているため、このアプリケーションは様々な最適化問題に対応することが可能です。具体的には、物流ルート最適化、スケジューリング、生産計画など、多くの実用的な問題に対する高速な解答を提供します。
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Typography variant="h3" gutterBottom className="section-title">
            どんなことができるのか
        </Typography>
        <List className="benefits-list">
            <ListItem>
                <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="物流ルート最適化" className="benefits-list-item"/>
            </ListItem>
            <Divider />
            <ListItem>
                <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="スケジューリング" className="benefits-list-item"/>
            </ListItem>
            <Divider />
            <ListItem>
                <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="生産計画" className="benefits-list-item"/>
            </ListItem>
            <Divider />
            <ListItem>
                <ListItemIcon>
                    <CheckCircleIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary="その他の最適化問題" className="benefits-list-item"/>
            </ListItem>
        </List>
      </Box>
    );
}

export default About;
