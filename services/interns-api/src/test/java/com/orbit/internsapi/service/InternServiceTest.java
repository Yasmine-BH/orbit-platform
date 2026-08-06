package com.orbit.internsapi.service;

import com.orbit.internsapi.dto.CreateInternRequest;
import com.orbit.internsapi.dto.InternResponse;
import com.orbit.internsapi.dto.UpdateInternRequest;
import com.orbit.internsapi.entity.Intern;
import com.orbit.internsapi.entity.InternStatus;
import com.orbit.internsapi.exception.DuplicateEmailException;
import com.orbit.internsapi.exception.InternNotFoundException;
import com.orbit.internsapi.repository.InternRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class InternServiceTest {

    @Mock
    private InternRepository internRepository;

    @InjectMocks
    private InternService internService;

    private Intern existingIntern;

    @BeforeEach
    void setUp() {
        existingIntern = new Intern(
                "Yasmine", "Ben Hamada", "yasmine@example.com",
                "ENIT", LocalDate.of(2026, 2, 1), InternStatus.ACTIVE
        );
    }

    @Test
    void create_savesAndReturnsIntern_whenEmailIsNew() {
        CreateInternRequest request = new CreateInternRequest(
                "Yasmine", "Ben Hamada", "yasmine@example.com",
                "ENIT", LocalDate.of(2026, 2, 1), InternStatus.ACTIVE
        );
        when(internRepository.existsByEmail(request.email())).thenReturn(false);
        when(internRepository.save(any(Intern.class))).thenReturn(existingIntern);

        InternResponse response = internService.create(request);

        assertThat(response.email()).isEqualTo("yasmine@example.com");
        assertThat(response.status()).isEqualTo(InternStatus.ACTIVE);
        verify(internRepository, times(1)).save(any(Intern.class));
    }

    @Test
    void create_throwsDuplicateEmail_whenEmailAlreadyExists() {
        CreateInternRequest request = new CreateInternRequest(
                "Yasmine", "Ben Hamada", "yasmine@example.com",
                "ENIT", LocalDate.of(2026, 2, 1), InternStatus.ACTIVE
        );
        when(internRepository.existsByEmail(request.email())).thenReturn(true);

        assertThatThrownBy(() -> internService.create(request))
                .isInstanceOf(DuplicateEmailException.class);
    }

    @Test
    void findById_returnsIntern_whenFound() {
        when(internRepository.findById(1L)).thenReturn(Optional.of(existingIntern));

        InternResponse response = internService.findById(1L);

        assertThat(response.email()).isEqualTo("yasmine@example.com");
    }

    @Test
    void findById_throwsNotFound_whenMissing() {
        when(internRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> internService.findById(99L))
                .isInstanceOf(InternNotFoundException.class);
    }

    @Test
    void findAll_returnsAllInterns() {
        when(internRepository.findAll()).thenReturn(List.of(existingIntern));

        List<InternResponse> responses = internService.findAll();

        assertThat(responses).hasSize(1);
    }

    @Test
    void update_updatesFields_whenInternExists() {
        UpdateInternRequest request = new UpdateInternRequest(
                "Yasmine", "Ben Hamada", "yasmine.new@example.com",
                "ENIT", LocalDate.of(2026, 2, 1), InternStatus.COMPLETED
        );
        when(internRepository.findById(1L)).thenReturn(Optional.of(existingIntern));
        when(internRepository.existsByEmail(anyString())).thenReturn(false);

        InternResponse response = internService.update(1L, request);

        assertThat(response.email()).isEqualTo("yasmine.new@example.com");
        assertThat(response.status()).isEqualTo(InternStatus.COMPLETED);
    }

    @Test
    void delete_removesIntern_whenFound() {
        when(internRepository.findById(1L)).thenReturn(Optional.of(existingIntern));

        internService.delete(1L);

        verify(internRepository, times(1)).delete(eq(existingIntern));
    }

    @Test
    void delete_throwsNotFound_whenMissing() {
        when(internRepository.findById(99L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> internService.delete(99L))
                .isInstanceOf(InternNotFoundException.class);
    }
}
