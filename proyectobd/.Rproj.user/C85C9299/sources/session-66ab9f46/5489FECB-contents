library(shiny)
library(shinydashboard)
library(ggplot2)
library(DT)
library(dplyr)

# Leer los datos desde el archivo CSV
datos <- read.csv("C:/Users/javis/OneDrive/Escritorio/8VO_SEMESTRE/Big_Data/proyecto_final_BD/WallCityTap_Consumer.csv")

# Definir la interfaz de usuario
ui <- dashboardPage(
  dashboardHeader(title = "Dashboard de Análisis de Consumidores"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Filtros", tabName = "filtros", icon = icon("filter")),
      # Filtro de edad
      sliderInput("filtroEdad", "Edad:", 
                  min = min(datos$Age), max = max(datos$Age), 
                  value = c(min(datos$Age), max(datos$Age))),
      # Filtro de métodos de pago
      checkboxGroupInput("filtroPago", "Medios de Pago:",
                         choices = c("Efectivo" = "Cash",
                                     "T. Crédito" = "Tcredit",
                                     "T. Débito" = "Tdebit"))
    )
  ),
  dashboardBody(
    fluidRow(
      box(title = "Edad promedio de consumidores que utilizan cada medio: Pago Electrónico", 
          dataTableOutput("dataSummary"), height = 250),
      box(title = "Segmentación: Método de Pago", 
          plotOutput("paymentMethodPlot", height = 250)),
      box(title = "Edad promedio de consumidores que poseen un ingreso anual mayor a $20,000", 
          dataTableOutput("highIncomeAge"), height = 250),
      box(title = "Conjunto de datos: Annual Income vs Spending Score", 
          dataTableOutput("dataTable"), height = 250)
    )
  )
)

# Definir el servidor
server <- function(input, output) {
  # Filtrar datos basados en la selección de edad
  datos_filtrados <- reactive({
    subset(datos, Age >= input$filtroEdad[1] & Age <= input$filtroEdad[2])
  })
  
  # Filtrar datos basados en los métodos de pago seleccionados
  observe({
    if (is.null(input$filtroPago)) {
      filtered_data <- datos_filtrados()
    } else {
      filtered_data <- datos_filtrados()[datos_filtrados()$Payment_Methods %in% input$filtroPago,]
    }
    # Actualizar la tabla de datos
    output$dataTable <- renderDataTable({
      datatable(filtered_data, options = list(pageLength = 5))
    })
  })
  
  # Gráfico de dispersión para el primer panel
  output$scatterPlot <- renderPlot({
    ggplot(datos_filtrados(), aes(x=Annual_Income, y=Spending_Score, color=Gender)) + 
      geom_point() +
      theme_minimal() +
      labs(title="Ingreso Anual vs Puntaje de Gasto", x="Ingreso Anual (k$)", y="Puntaje de Gasto (1-100)")
  })
  
  # Resumen de datos para el segundo panel
  output$dataSummary <- renderDataTable({
    # Calcular el promedio de edad para cada método de pago
    data_summary <- datos_filtrados() %>%
      group_by(Payment_Methods) %>%
      summarise(Age_Mean = mean(Age, na.rm = TRUE))
    
    datatable(data_summary, options = list(pageLength = 5))
  })
  
  # Gráfico de dispersión para el panel de segmentación por método de pago
  output$paymentMethodPlot <- renderPlot({
    ggplot(datos_filtrados(), aes(x=Annual_Income, y=Age, color=Payment_Methods)) + 
      geom_point() +
      theme_minimal() +
      labs(title="Segmentación: Método de Pago", x="Ingreso Anual", y="Edad")
  })
  
  # Tabla de edad promedio para consumidores con ingreso anual mayor a $20,000
  output$highIncomeAge <- renderDataTable({
    # Filtrar consumidores con ingreso anual mayor a $20,000
    high_income_consumers <- datos_filtrados() %>%
      filter(Annual_Income > 20) %>%
      summarise(Average_Age = mean(Age, na.rm = TRUE))
    
    datatable(high_income_consumers, options = list(pageLength = 5))
  })
}

# Ejecutar la aplicación
shinyApp(ui, server)


