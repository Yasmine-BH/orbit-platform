package com.orbit.internsapi.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.orbit.internsapi.dto.CreateInternRequest;
import com.orbit.internsapi.dto.InternResponse;
import com.orbit.internsapi.entity.InternStatus;
import com.orbit.internsapi.exception.InternNotFoundException;
import com.orbit.internsapi.service.InternService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(InternController.class)
class InternControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private InternService internService;

    private InternResponse sampleResponse() {
        return new InternResponse(
                1L, "Yasmine", "Ben Hamada", "yasmine@example.com",
                "ENIT", LocalDate.of(2026, 2, 1), InternStatus.ACTIVE
        );
    }

    @Test
    void createIntern_returns201_whenRequestIsValid() throws Exception {
        CreateInternRequest request = new CreateInternRequest(
                "Yasmine", "Ben Hamada", "yasmine@example.com",
                "ENIT", LocalDate.of(2026, 2, 1), InternStatus.ACTIVE
        );
        when(internService.create(any())).thenReturn(sampleResponse());

        mockMvc.perform(post("/api/interns")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.email").value("yasmine@example.com"));
    }

    @Test
    void createIntern_returns400_whenEmailIsInvalid() throws Exception {
        String badPayload = """
                {
                  "firstName": "Yasmine",
                  "lastName": "Ben Hamada",
                  "email": "not-an-email",
                  "university": "ENIT",
                  "startDate": "2026-02-01",
                  "status": "ACTIVE"
                }
                """;

        mockMvc.perform(post("/api/interns")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(badPayload))
                .andExpect(status().isBadRequest());
    }

    @Test
    void getIntern_returns200_whenFound() throws Exception {
        when(internService.findById(1L)).thenReturn(sampleResponse());

        mockMvc.perform(get("/api/interns/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.firstName").value("Yasmine"));
    }

    @Test
    void getIntern_returns404_whenMissing() throws Exception {
        when(internService.findById(99L)).thenThrow(new InternNotFoundException(99L));

        mockMvc.perform(get("/api/interns/99"))
                .andExpect(status().isNotFound());
    }

    @Test
    void listInterns_returnsAll() throws Exception {
        when(internService.findAll()).thenReturn(List.of(sampleResponse()));

        mockMvc.perform(get("/api/interns"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1));
    }

    @Test
    void deleteIntern_returns204() throws Exception {
        mockMvc.perform(delete("/api/interns/1"))
                .andExpect(status().isNoContent());
    }
}
