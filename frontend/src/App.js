import React from 'react';
import './App.css';
import Header from './Components/Header'; // Adjusted path
import Sidebar from './Components/SideBar'; // Import Sidebar
import Body from './Components/Body'; // Import Body
import { Container, Row, Col } from 'react-bootstrap';

function App() {
  return (
    <div className="App">
      <Header />
      <Container fluid>
        <Row>
          <Col xs={2} id="sidebar-wrapper">      
            <Sidebar />
          </Col>
          <Col xs={10} id="page-content-wrapper">
            <Body />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
