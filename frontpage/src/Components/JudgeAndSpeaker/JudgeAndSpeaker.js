import React from "react";
import { Row, Col } from "react-bootstrap";
import styled from "styled-components";
const Wrapper = styled.div`
  padding: 60px 0;
  .title {
    font-family: "Avenir";
    font-style: normal;
    font-weight: 300;
    font-size: 80px;
    line-height: 130%;
    color: #ffffff;
  }
  .member {
    width: 150px;
    height: 150px;

    border-radius: 50%;

    background: rgba(0, 0, 0, 0.33);
  }
  @media only screen and (max-width: 1600px) {
    .member {
      width: 140px;
      height: 140px;
    }
  }
  @media only screen and (max-width: 1399px) {
    .title {
      font-size: 55px;
    }
    .member {
      width: 180px;
      height: 180px;
    }
  }
  @media only screen and (max-width: 767px) {
    padding-top: 45px;
    .title {
      font-size: 50px;
    }
    .member {
      width: 150px;
      height: 150px;
    }
  }
  @media only screen and (max-width: 520px) {
    .title {
      font-size: 35px;
    }
  }
  @media only screen and (max-width: 400px) {
    .member {
      width: 140px;
      height: 140px;
    }
  }
`;
const JudgeAndSpeaker = () => {
  const judgeAndspeaker = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}];
  return (
    <Wrapper id="team">
      <Col
        xs={11}
        md={10}
        xl={9}
        xxl={8}
        className="d-flex flex-column justify-content-center mx-auto"
      >
        <h2 className="title text-center">judges and speakers</h2>
        <Row className="d-flex  justify-content-center align-items-center py-5">
          {judgeAndspeaker.map((el, i) => (
            <Col
              xs={6}
              sm={4}
              md={4}
              lg={3}
              xl={3}
              xxl={2}
              key={i}
              className=" my-3 d-flex justify-content-center"
            >
              <div className="member "></div>
            </Col>
          ))}
        </Row>
      </Col>
    </Wrapper>
  );
};
export default JudgeAndSpeaker;
