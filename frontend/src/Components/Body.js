import React from 'react';
import ScatterPlot from './ScatterPlot'; // Adjust the import path as needed

const Body = () => {
    return (
        <div className="container-fluid">
            <div className="row content">
                <div className="col-sm-9">
                    <div>
                        <h2>Car Data Scatter Plot</h2>
                        <ScatterPlot />
                    </div>
                    <div className="row">
                        <div className="col-sm-3">
                            <div className="well">
                                <h4>Users</h4>
                                <ScatterPlot />
                            </div>
                        </div>
                        <div className="col-sm-3">
                            <div className="well">
                                <h4>Pages</h4>
                                <ScatterPlot />
                            </div>
                        </div>
                        <div className="col-sm-3">
                            <div className="well">
                                <h4>Sessions</h4>
                                <ScatterPlot />
                            </div>
                        </div>
                        <div className="col-sm-3">
                            <div className="well">
                                <h4>Bounce</h4>
                                <ScatterPlot />
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-4">
                            <div className="well">
                                <ScatterPlot />
                            </div>
                        </div>
                        <div className="col-sm-4">
                            <div className="well">
                            <ScatterPlot />
                            </div>
                        </div>
                        <div className="col-sm-4">
                            <div className="well">
                            <ScatterPlot />
                            </div>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-sm-8">
                            <div className="well">
                            <ScatterPlot />
                            </div>
                        </div>
                        <div className="col-sm-4">
                            <div className="well">
                            <ScatterPlot />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Body;
