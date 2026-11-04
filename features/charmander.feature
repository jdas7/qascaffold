Feature: Recurso público de Charmander

  Scenario: Consultar el recurso público de Charmander
    When se consulta el pokemon "charmander"
    Then la respuesta tiene estado 200
    And el nombre es "charmander"
    And el id es 4
    And los tipos incluyen "fire"
