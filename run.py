from main import *
import time


M = Mandelbrot()

running = True

while running:

    for event in M.pygame.event.get():

        if event.type == M.pygame.QUIT:
            running = False
            M.pygame.quit()

        elif event.type == M.pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = event.pos
            start_surface = M.pygame.display.get_surface().copy()
            clicking = True

        elif event.type == M.pygame.MOUSEBUTTONUP and event.button == 1:
            end_pos = event.pos
            clicking = False
            M.zoom(start_pos, end_pos)

        elif event.type == M.pygame.KEYDOWN:

            if event.key == M.pygame.K_c:
                M.change_colors()

            if event.key == M.pygame.K_v:
                M.previous_colors()

            if event.key == M.pygame.K_a:
                M.increase_oscillations()

            if event.key == M.pygame.K_z:
                M.reduce_oscillations()

            if event.key == M.pygame.K_e:
                M.increase_shift()

            if event.key == M.pygame.K_t:
                M.decrease_shift()

            if event.key == M.pygame.K_SPACE:
                M.double_iterations()

            if event.key == M.pygame.K_b:
                M.half_iterations()

            if event.key == M.pygame.K_t:
                M.three_halfs_iterations()

            if event.key == M.pygame.K_LEFT:
                M.back()

            if event.key == M.pygame.K_RIGHT:
                M.forward()

            if event.key == M.pygame.K_s:
                M.save()

            if event.key == M.pygame.K_q:
                M.quality_save()

            if event.key == M.pygame.K_BACKSPACE:
                M.restart()

            if event.key == M.pygame.K_y:
                M.draw_future_zoom()

            if event.key == M.pygame.K_i:
                M.info_displayed = not M.info_displayed
                M.plot()

            if event.key == M.pygame.K_h:
                M.help_displayed = not M.help_displayed
                M.plot()

            if event.key == M.pygame.K_x:
                M.change_transformation_right()

            if event.key == M.pygame.K_w:
                M.change_transformation_left()

            if event.key == M.pygame.K_j:
                M.change_fractal()

            if event.key == M.pygame.K_u:
                M.up_c()

            if event.key == M.pygame.K_d:
                M.down_c()

            if event.key == M.pygame.K_r:
                M.right_c()

            if event.key == M.pygame.K_l:
                M.left_c()

            if event.key == M.pygame.K_n:
                M.up_delta_c()

            if event.key == M.pygame.K_k:
                M.down_delta_c()

        elif event.type == M.pygame.KEYUP:

            if event.key == M.pygame.K_y:
                M.plot()
        else:
            keys = M.pygame.key.get_pressed()

            if keys[M.pygame.K_p]:
                M.increase_shift()

            if keys[M.pygame.K_m]:
                M.decrease_shift()

    try:

        if clicking:
            current_pos = M.pygame.mouse.get_pos()
            M.screen.blit(start_surface, (0, 0))
            M.draw_rectangle_from_pos(start_pos, current_pos)
            M.display.update()

    except NameError:
        pass


