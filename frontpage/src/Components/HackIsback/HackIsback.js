import React from 'react';
import { Row, Col } from 'react-bootstrap';
import styled from 'styled-components';
const Wrapper = styled.div`
    padding: 90px 0;

    .title {
        font-family: 'Avenir';

        font-weight: 300;
        font-size: 80px;
        line-height: 120%;

        color: #ffffff;
    }
    .icon {
        width: 90px;
        height: 100px;
        object-fit: cover;
    }
    .number {
        font-family: Avenir;
        font-style: normal;
        font-weight: 500;
        font-size: 50px;
        line-height: 130%;
        text-align: center;

        color: #ffffff;
    }
    .name {
        font-family: Blinker;
        font-style: normal;
        font-weight: 200;
        font-size: 35px;
        line-height: 130%;

        color: rgba(255, 255, 255, 1);
    }
    @media only screen and (max-width: 1600px) {
        .icon {
            width: 70px;
            height: 75px;
        }
        .number {
            font-size: 40px;
        }
        .name {
            font-size: 27px;
        }
    }
    @media only screen and (max-width: 1399px) {
        .title {
            font-size: 55px;
        }
        .icon {
            width: 70px;
            height: 75px;
        }
        .number {
            font-size: 40px;
        }
        .name {
            font-size: 27px;
        }
    }
    @media only screen and (max-width: 767px) {
        padding-bottm: 45px;
        .title {
            font-size: 50px;
        }
    }
    @media only screen and (max-width: 520px) {
        .title {
            font-size: 40px;
        }
    }
`;
const HackIsback = () => {
    const cardArray = [
        {
            icon: './images/time.png',
            number: '36',
            name: 'hours of fun challenges',
        },
        {
            icon: './images/prize.png',
            number: '$5,000',
            name: 'in prizes',
        },
        {
            icon: './images/mail.png',
            number: '1',
            name: 'pinnacle invitation',
        },
    ];
    return (
        <Wrapper>
            {' '}
            <Col
                xs={11}
                md={10}
                xl={9}
                xxl={8}
                className="d-flex flex-column justify-content-center mx-auto"
            >
                <h4 className="title text-center pb-3  pb-md-5 ">
                    los altos hacks is back.
                </h4>

                <Row className="py-5">
                    {cardArray.map((el, i) => (
                        <Col
                            md={4}
                            className="d-flex flex-column justify-content-center align-items-center my-3 my-0"
                            key={i}
                        >
                            <img src={el.icon} alt="" className="icon" />
                            <div
                                className="d-flex flex-column "
                                style={{ height: '100%' }}
                            >
                                <p className="number text-center py-3 pb-2">
                                    {el.number}
                                </p>
                                <p
                                    className="name text-center "
                                    style={{ paddingTop: i === 2 && '10px' }}
                                >
                                    {el.name}
                                </p>
                            </div>
                        </Col>
                    ))}
                </Row>
            </Col>
        </Wrapper>
    );
};
export default HackIsback;
