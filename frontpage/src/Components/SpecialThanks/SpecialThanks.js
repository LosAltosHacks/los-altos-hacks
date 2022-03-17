import React from 'react';
import { Row, Col } from 'react-bootstrap';
import styled from 'styled-components';
const Wrapper = styled.div`
    height: 800px;
    .title {
        font-family: 'Avenir';
        font-style: normal;
        font-weight: 300;
        font-size: 80px;
        line-height: 109px;

        color: #ffffff;
    }
    @media only screen and (max-width: 767px) {
        .title {
            font-size: 55px;
        }
    }
    @media only screen and (max-width: 767px) {
        .title {
            font-size: 50px;
        }
    }
    @media only screen and (max-width: 520px) {
        .title {
            font-size: 35px;
        }
    }
`;
const SpecialThanks = () => {
    return (
        <Wrapper id="sponsors">
            <Col
                xs={11}
                sm={9}
                md={7}
                xxl={5}
                className="d-flex flex-column justify-content-center mx-auto"
            >
                <h2 className="title text-center">Speacial Thanks</h2>
            </Col>
        </Wrapper>
    );
};
export default SpecialThanks;
