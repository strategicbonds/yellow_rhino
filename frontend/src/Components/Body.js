import React from 'react';
import ScatterPlot from './PlotScatter'; // Adjust the import path as needed
import ScatterPlot3D from './PlotScatter3d';


const Body = () => {
    return (
        <div className="container-fluid">
            <div className="row content">
                <div className="col-sm-9">
                    <div>
                        <h2>Car Data Scatter Plot</h2>
                        <ScatterPlot3D />
                    </div>
                    <div className="row">
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
