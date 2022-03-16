import React from "react";
import { Row, Col } from "react-bootstrap";
import styled from "styled-components";
const Wrapper = styled.div`
  padding: 90px 0;
  padding-top: 140px;
  .tagline {
    font-family: Blinker;
    font-style: normal;
    font-weight: 200;
    font-size: 70px;
    line-height: 150%;

    color: rgba(255, 255, 255, 0.6);
  }
  .title {
    align-self: flex-end;
  }
  .image {
    width: 100%;
  }
  @media only screen and (max-width: 1399px) {
    .tagline {
      font-size: 50px;
      line-height: 130%;
    }
    .title {
      align-self: flex-end;
      font-size: 55px;
    }
  }
  @media only screen and (max-width: 767px) {
    padding: 40px 0;
    padding-top: 110px;
    .tagline {
      font-size: 45px;
    }
    .title {
      font-size: 50px;
    }
  }
  @media only screen and (max-width: 520px) {
    .tagline {
      font-size: 40px;
    }
    .title {
      font-size: 35px;
      line-height: 150%;
    }
  }
`;
const HeroSection = () => {
  return (
    <Wrapper id="register">
      <Col
        xs={11}
        sm={9}
        md={7}
        xxl={5}
        className="d-flex flex-column justify-content-center mx-auto"
      >
        <h4 className="tagline">via Discord</h4>
        <img src="./images/hero.png" alt="#" className="image" />
        <h4 className="title">april 24 - 26</h4>
      </Col>
    </Wrapper>
  );
};
export default HeroSection;
