class PlantsController < ApplicationController

  def index
    render json: Plant.all
  end

  def show
    plant = Plant.find_by(id: params[:id])
    render json: plant
  end

  def create
    plant = Plant.create(plant_params)
    render json: plant
  end

  private

  def plant_params
    params.permit(:id, :image, :price, :name)
  end
end
