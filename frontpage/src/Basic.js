import React from 'react';
import { Row, Col } from 'react-bootstrap';
import styled from 'styled-components';
const Wrapper = styled.div``;
const Basic = () => {
    return (
        <Wrapper>
            <Col
                xs={11}
                sm={9}
                md={7}
                xxl={5}
                className="d-flex flex-column justify-content-center mx-auto"
            ></Col>
        </Wrapper>
    );
};
export default Basic;
